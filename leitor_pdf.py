"""
VHALINOR Leitor de PDFs v6.0
=============================
Sistema de leitura e processamento de PDFs para ai_geral:
- Leitura de PDFs locais e da rede (URLs)
- Extração de texto, imagens e metadados
- Análise de conteúdo e sumarização
- Indexação para busca
- Processamento em lote
- Cache de documentos
- Conversão para outros formatos
- OCR para PDFs scanned
- Integração com NLP para análise

@module leitor_pdf
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable, BinaryIO
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque
import hashlib
import json
import os
import re
import tempfile
import io
import warnings

# Imports opcionais com fallback
PDFPLUMBER_AVAILABLE = False
PYPDF2_AVAILABLE = False
PDFMINER_AVAILABLE = False
PILLOW_AVAILABLE = False
PYTESSERACT_AVAILABLE = False
REQUESTS_AVAILABLE = False
Fitz_AVAILABLE = False

# Tentar importar bibliotecas de PDF
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    pdfplumber = None

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PyPDF2 = None

try:
    from pdfminer.high_level import extract_text
    PDFMINER_AVAILABLE = True
except ImportError:
    extract_text = None

try:
    import fitz  # PyMuPDF
    Fitz_AVAILABLE = True
except ImportError:
    fitz = None

# Para downloads
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    requests = None

# Para OCR
try:
    from PIL import Image
    PILLOW_AVAILABLE = True
except ImportError:
    Image = None

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None

warnings.filterwarnings("ignore")


class TipoPDF(Enum):
    """Tipos de PDF baseado no conteúdo"""
    TEXTO = "texto"           # PDF com texto selecionável
    SCANNEADO = "scanned"     # PDF de imagem (necessita OCR)
    MISTO = "misto"           # Mistura de texto e imagens
    FORMULARIO = "formulario" # PDF com campos de formulário
    APRESENTACAO = "apresentacao"
    RELATORIO = "relatorio"
    ARTIGO = "artigo"
    LIVRO = "livro"
    DOCUMENTO_TECNICO = "documento_tecnico"


class StatusProcessamento(Enum):
    """Status do processamento de um PDF"""
    PENDENTE = "pendente"
    BAIXANDO = "baixando"
    PROCESSANDO = "processando"
    EXTRAINDO_TEXTO = "extraindo_texto"
    APLICANDO_OCR = "aplicando_ocr"
    ANALISANDO = "analisando"
    CONCLUIDO = "concluido"
    ERRO = "erro"


@dataclass
class MetadadosPDF:
    """Metadados de um documento PDF"""
    titulo: Optional[str] = None
    autor: Optional[str] = None
    assunto: Optional[str] = None
    criador: Optional[str] = None
    produtor: Optional[str] = None
    data_criacao: Optional[str] = None
    data_modificacao: Optional[str] = None
    numero_paginas: int = 0
    palavras_chave: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "titulo": self.titulo,
            "autor": self.autor,
            "assunto": self.assunto,
            "criador": self.criador,
            "produtor": self.produtor,
            "data_criacao": self.data_criacao,
            "data_modificacao": self.data_modificacao,
            "numero_paginas": self.numero_paginas,
            "palavras_chave": self.palavras_chave
        }


@dataclass
class PaginaPDF:
    """Representação de uma página de PDF"""
    numero: int
    texto: str = ""
    tem_imagem: bool = False
    imagens: List[Dict[str, Any]] = field(default_factory=list)
    tabelas: List[List[List[str]]] = field(default_factory=list)
    dimensoes: Tuple[float, float] = (0.0, 0.0)  # largura, altura
    
    @property
    def num_palavras(self) -> int:
        return len(self.texto.split())
    
    @property
    def num_caracteres(self) -> int:
        return len(self.texto)


@dataclass
class DocumentoPDF:
    """Documento PDF processado"""
    id: str
    url: Optional[str] = None
    caminho_local: Optional[str] = None
    nome_arquivo: str = ""
    tipo: TipoPDF = TipoPDF.TEXTO
    metadados: MetadadosPDF = field(default_factory=MetadadosPDF)
    paginas: List[PaginaPDF] = field(default_factory=list)
    texto_completo: str = ""
    hash_conteudo: str = ""
    tamanho_bytes: int = 0
    status: StatusProcessamento = StatusProcessamento.PENDENTE
    data_processamento: Optional[str] = None
    erros: List[str] = field(default_factory=list)
    
    @property
    def num_paginas(self) -> int:
        return len(self.paginas)
    
    @property
    def num_palavras_total(self) -> int:
        return sum(p.num_palavras for p in self.paginas)
    
    def obter_resumo(self, max_palavras: int = 100) -> str:
        """Obter resumo do conteúdo"""
        texto = self.texto_completo[:max_palavras * 10]
        palavras = texto.split()[:max_palavras]
        return " ".join(palavras) + ("..." if len(self.texto_completo) > len(" ".join(palavras)) else "")
    
    def buscar_termo(self, termo: str, case_sensitive: bool = False) -> List[Tuple[int, str]]:
        """Buscar termo em todas as páginas"""
        resultados = []
        flags = 0 if case_sensitive else re.IGNORECASE
        
        for pagina in self.paginas:
            if re.search(termo, pagina.texto, flags):
                # Encontrar contexto
                matches = list(re.finditer(termo, pagina.texto, flags))
                for match in matches:
                    inicio = max(0, match.start() - 50)
                    fim = min(len(pagina.texto), match.end() + 50)
                    contexto = pagina.texto[inicio:fim]
                    resultados.append((pagina.numero, contexto))
        
        return resultados


@dataclass
class AnaliseConteudoPDF:
    """Análise do conteúdo de um PDF"""
    documento_id: str
    tema_principal: Optional[str] = None
    temas_secundarios: List[str] = field(default_factory=list)
    entidades_nomeadas: Dict[str, List[str]] = field(default_factory=dict)  # pessoas, locais, organizações
    sentimento_geral: str = "neutro"  # positivo, negativo, neutro
    complexidade_leitura: float = 0.0  # 0-1, sendo 1 mais complexo
    resumo_executivo: str = ""
    palavras_chave: List[str] = field(default_factory=list)
    estatisticas: Dict[str, Any] = field(default_factory=dict)


class LeitorPDF:
    """
    Sistema de leitura e processamento de PDFs da VHALINOR ai_geral.
    
    Permite ler PDFs de arquivos locais ou URLs, extrair texto,
    aplicar OCR quando necessário, e analisar conteúdo.
    """
    
    def __init__(self, diretorio_cache: Optional[str] = None):
        self.nome = "VHALINOR Leitor PDF"
        self.versao = "6.0.0"
        
        # Cache
        self.diretorio_cache = diretorio_cache or tempfile.gettempdir()
        self.cache_documentos: Dict[str, DocumentoPDF] = {}
        
        # Documentos processados
        self.documentos: Dict[str, DocumentoPDF] = {}
        self.historico_downloads: deque = deque(maxlen=100)
        
        # Configurações
        self.timeout_download = 30
        self.max_tamanho_mb = 100
        self.usar_ocr = PYTESSERACT_AVAILABLE
        
        # Métricas
        self.total_pdfs_processados = 0
        self.total_paginas_processadas = 0
        self.total_downloads = 0
        self.erros_processamento = 0
        
        # Callbacks
        self._on_documento_processado: List[Callable] = []
        self._on_erro_processamento: List[Callable] = []
    
    def _baixar_pdf(self, url: str, nome_arquivo: Optional[str] = None) -> Optional[str]:
        """Baixar PDF de URL"""
        if not REQUESTS_AVAILABLE or requests is None:
            return None
        
        try:
            # Verificar se é URL válida
            if not url.startswith(('http://', 'https://', 'ftp://')):
                return None
            
            # Fazer download
            response = requests.get(
                url,
                timeout=self.timeout_download,
                stream=True,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            response.raise_for_status()
            
            # Verificar tamanho
            tamanho = int(response.headers.get('content-length', 0))
            if tamanho > self.max_tamanho_mb * 1024 * 1024:
                return None
            
            # Determinar nome do arquivo
            if not nome_arquivo:
                # Tentar extrair do header
                content_disposition = response.headers.get('content-disposition', '')
                if 'filename=' in content_disposition:
                    nome_arquivo = content_disposition.split('filename=')[1].strip('"\'')
                else:
                    # Usar hash da URL
                    nome_arquivo = hashlib.md5(url.encode()).hexdigest()[:12] + ".pdf"
            
            # Salvar arquivo
            caminho = os.path.join(self.diretorio_cache, nome_arquivo)
            with open(caminho, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            self.total_downloads += 1
            self.historico_downloads.append({
                "url": url,
                "caminho": caminho,
                "data": datetime.now(timezone.utc).isoformat(),
                "tamanho": tamanho
            })
            
            return caminho
            
        except Exception as e:
            return None
    
    def _extrair_metadados(self, caminho: str) -> MetadadosPDF:
        """Extrair metadados do PDF"""
        metadados = MetadadosPDF()
        
        try:
            if Fitz_AVAILABLE and fitz is not None:
                doc = fitz.open(caminho)
                info = doc.metadata
                
                metadados.titulo = info.get("title")
                metadados.autor = info.get("author")
                metadados.assunto = info.get("subject")
                metadados.criador = info.get("creator")
                metadados.produtor = info.get("producer")
                metadados.data_criacao = info.get("creationDate")
                metadados.data_modificacao = info.get("modDate")
                metadados.numero_paginas = len(doc)
                
                doc.close()
                
            elif PYPDF2_AVAILABLE and PyPDF2 is not None:
                with open(caminho, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    info = reader.metadata
                    
                    if info:
                        metadados.titulo = info.get("/Title")
                        metadados.autor = info.get("/Author")
                        metadados.assunto = info.get("/Subject")
                        metadados.criador = info.get("/Creator")
                        metadados.produtor = info.get("/Producer")
                    
                    metadados.numero_paginas = len(reader.pages)
                    
        except Exception:
            pass
        
        return metadados
    
    def _extrair_texto_pdfplumber(self, caminho: str) -> List[PaginaPDF]:
        """Extrair texto usando pdfplumber"""
        paginas = []
        
        if not PDFPLUMBER_AVAILABLE or pdfplumber is None:
            return paginas
        
        try:
            with pdfplumber.open(caminho) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    texto = page.extract_text() or ""
                    
                    pagina = PaginaPDF(
                        numero=i,
                        texto=texto,
                        dimensoes=(page.width, page.height)
                    )
                    
                    # Extrair tabelas
                    tabelas = page.extract_tables()
                    if tabelas:
                        pagina.tabelas = tabelas
                    
                    # Verificar se tem imagens
                    imagens = page.images
                    if imagens:
                        pagina.tem_imagem = True
                        pagina.imagens = [{"bbox": img} for img in imagens]
                    
                    paginas.append(pagina)
                    
        except Exception:
            pass
        
        return paginas
    
    def _extrair_texto_fitz(self, caminho: str) -> List[PaginaPDF]:
        """Extrair texto usando PyMuPDF (fitz)"""
        paginas = []
        
        if not Fitz_AVAILABLE or fitz is None:
            return paginas
        
        try:
            doc = fitz.open(caminho)
            
            for i in range(len(doc)):
                page = doc[i]
                texto = page.get_text()
                
                pagina = PaginaPDF(
                    numero=i + 1,
                    texto=texto,
                    dimensoes=(page.rect.width, page.rect.height)
                )
                
                # Verificar imagens
                images = page.get_images()
                if images:
                    pagina.tem_imagem = True
                    pagina.imagens = [{"xref": img[0]} for img in images]
                
                paginas.append(pagina)
            
            doc.close()
            
        except Exception:
            pass
        
        return paginas
    
    def _extrair_texto_pypdf2(self, caminho: str) -> List[PaginaPDF]:
        """Extrair texto usando PyPDF2 (fallback)"""
        paginas = []
        
        if not PYPDF2_AVAILABLE or PyPDF2 is None:
            return paginas
        
        try:
            with open(caminho, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                
                for i, page in enumerate(reader.pages):
                    texto = page.extract_text() or ""
                    
                    pagina = PaginaPDF(
                        numero=i + 1,
                        texto=texto
                    )
                    paginas.append(pagina)
                    
        except Exception:
            pass
        
        return paginas
    
    def _aplicar_ocr(self, caminho: str, paginas: List[PaginaPDF]) -> List[PaginaPDF]:
        """Aplicar OCR em páginas com pouco ou nenhum texto"""
        if not self.usar_ocr or not Fitz_AVAILABLE or not PYTESSERACT_AVAILABLE:
            return paginas
        
        try:
            doc = fitz.open(caminho)
            
            for pagina in paginas:
                # Se página tem pouco texto, aplicar OCR
                if len(pagina.texto.strip()) < 100:
                    page = doc[pagina.numero - 1]
                    
                    # Renderizar página como imagem
                    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom para melhor OCR
                    img_data = pix.tobytes("png")
                    
                    # Aplicar OCR
                    if PILLOW_AVAILABLE and Image is not None:
                        img = Image.open(io.BytesIO(img_data))
                        texto_ocr = pytesseract.image_to_string(img, lang='por+eng')
                        
                        if texto_ocr.strip():
                            pagina.texto += "\n[OCR]\n" + texto_ocr
                            pagina.tem_imagem = True
            
            doc.close()
            
        except Exception:
            pass
        
        return paginas
    
    def processar_pdf(
        self,
        fonte: str,
        nome_arquivo: Optional[str] = None,
        aplicar_ocr: bool = True,
        forcar_download: bool = False
    ) -> Optional[DocumentoPDF]:
        """
        Processar um PDF de arquivo local ou URL.
        
        Args:
            fonte: Caminho local ou URL do PDF
            nome_arquivo: Nome opcional para o arquivo
            aplicar_ocr: Se deve aplicar OCR em páginas scannadas
            forcar_download: Se deve baixar mesmo se já estiver em cache
        
        Returns:
            DocumentoPDF processado ou None em caso de erro
        """
        # Gerar ID único
        doc_id = hashlib.md5(f"{fonte}{datetime.now()}".encode()).hexdigest()[:16]
        
        # Verificar se é URL
        eh_url = fonte.startswith(('http://', 'https://', 'ftp://'))
        
        caminho_local = None
        url = None
        
        if eh_url:
            url = fonte
            # Verificar cache
            if not forcar_download:
                for doc in self.cache_documentos.values():
                    if doc.url == url:
                        return doc
            
            # Baixar
            caminho_local = self._baixar_pdf(url, nome_arquivo)
            if not caminho_local:
                return None
        else:
            caminho_local = fonte
            if not os.path.exists(caminho_local):
                return None
        
        # Criar documento
        documento = DocumentoPDF(
            id=doc_id,
            url=url,
            caminho_local=caminho_local,
            nome_arquivo=os.path.basename(caminho_local),
            status=StatusProcessamento.PROCESSANDO
        )
        
        try:
            # Obter tamanho
            documento.tamanho_bytes = os.path.getsize(caminho_local)
            
            # Extrair metadados
            documento.status = StatusProcessamento.EXTRAINDO_TEXTO
            documento.metadados = self._extrair_metadados(caminho_local)
            
            # Extrair texto
            # Tentar pdfplumber primeiro (melhor para tabelas)
            paginas = self._extrair_texto_pdfplumber(caminho_local)
            
            # Se falhou ou poucas páginas, tentar fitz
            if not paginas or len(paginas) < documento.metadados.numero_paginas // 2:
                paginas = self._extrair_texto_fitz(caminho_local)
            
            # Fallback para PyPDF2
            if not paginas:
                paginas = self._extrair_texto_pypdf2(caminho_local)
            
            # Aplicar OCR se necessário
            if aplicar_ocr and self.usar_ocr:
                documento.status = StatusProcessamento.APLICANDO_OCR
                paginas = self._aplicar_ocr(caminho_local, paginas)
            
            documento.paginas = paginas
            documento.texto_completo = "\n\n".join(p.texto for p in paginas)
            documento.hash_conteudo = hashlib.md5(documento.texto_completo.encode()).hexdigest()
            
            # Determinar tipo
            if any(p.tem_imagem for p in paginas):
                if all(len(p.texto.strip()) < 100 for p in paginas[:3]):
                    documento.tipo = TipoPDF.SCANNEADO
                else:
                    documento.tipo = TipoPDF.MISTO
            else:
                documento.tipo = TipoPDF.TEXTO
            
            documento.status = StatusProcessamento.CONCLUIDO
            documento.data_processamento = datetime.now(timezone.utc).isoformat()
            
            # Armazenar
            self.documentos[doc_id] = documento
            if url:
                self.cache_documentos[doc_id] = documento
            
            # Atualizar métricas
            self.total_pdfs_processados += 1
            self.total_paginas_processadas += len(paginas)
            
            # Notificar
            for callback in self._on_documento_processado:
                callback(documento)
            
            return documento
            
        except Exception as e:
            documento.status = StatusProcessamento.ERRO
            documento.erros.append(str(e))
            self.erros_processamento += 1
            
            for callback in self._on_erro_processamento:
                callback(documento, str(e))
            
            return None
    
    def processar_multiplos(
        self,
        fontes: List[str],
        max_workers: int = 3
    ) -> List[DocumentoPDF]:
        """Processar múltiplos PDFs"""
        documentos = []
        
        for fonte in fontes:
            doc = self.processar_pdf(fonte)
            if doc:
                documentos.append(doc)
        
        return documentos
    
    def analisar_conteudo(self, documento_id: str) -> Optional[AnaliseConteudoPDF]:
        """Analisar conteúdo de um documento"""
        if documento_id not in self.documentos:
            return None
        
        doc = self.documentos[documento_id]
        
        analise = AnaliseConteudoPDF(
            documento_id=documento_id,
            resumo_executivo=doc.obter_resumo(200)
        )
        
        # Extrair palavras-chave simples (frequência)
        texto = doc.texto_completo.lower()
        palavras = re.findall(r'\b[a-z]{4,}\b', texto)
        
        # Contar frequência
        freq = {}
        for palavra in palavras:
            if palavra not in ['esse', 'essa', 'isso', 'aquele', 'aquela', 'para', 'como', 'onde', 'quando', 'pelo', 'pela']:
                freq[palavra] = freq.get(palavra, 0) + 1
        
        # Top palavras-chave
        analise.palavras_chave = [p for p, _ in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]]
        
        # Estatísticas
        analise.estatisticas = {
            "total_paginas": doc.num_paginas,
            "total_palavras": doc.num_palavras_total,
            "media_palavras_por_pagina": doc.num_palavras_total / max(1, doc.num_paginas),
            "tem_imagens": any(p.tem_imagem for p in doc.paginas),
            "tem_tabelas": any(p.tabelas for p in doc.paginas)
        }
        
        return analise
    
    def buscar_em_documentos(self, termo: str) -> List[Tuple[str, int, str]]:
        """Buscar termo em todos os documentos processados"""
        resultados = []
        
        for doc_id, doc in self.documentos.items():
            matches = doc.buscar_termo(termo)
            for pagina_num, contexto in matches:
                resultados.append((doc.nome_arquivo, pagina_num, contexto))
        
        return resultados
    
    def exportar_texto(self, documento_id: str, formato: str = "txt") -> Optional[str]:
        """Exportar texto do documento para formato especificado"""
        if documento_id not in self.documentos:
            return None
        
        doc = self.documentos[documento_id]
        
        if formato == "txt":
            return doc.texto_completo
        
        elif formato == "json":
            return json.dumps({
                "metadados": doc.metadados.to_dict(),
                "paginas": [
                    {
                        "numero": p.numero,
                        "texto": p.texto,
                        "num_palavras": p.num_palavras
                    }
                    for p in doc.paginas
                ],
                "texto_completo": doc.texto_completo
            }, ensure_ascii=False, indent=2)
        
        elif formato == "markdown":
            md = f"# {doc.metadados.titulo or doc.nome_arquivo}\n\n"
            md += f"**Autor:** {doc.metadados.autor or 'Desconhecido'}\n\n"
            md += f"**Páginas:** {doc.num_paginas}\n\n"
            md += "---\n\n"
            
            for pagina in doc.paginas:
                md += f"## Página {pagina.numero}\n\n"
                md += pagina.texto + "\n\n"
            
            return md
        
        return None
    
    def limpar_cache(self, max_idade_dias: int = 7):
        """Limpar arquivos de cache antigos"""
        limpos = 0
        
        try:
            for arquivo in os.listdir(self.diretorio_cache):
                if arquivo.endswith('.pdf'):
                    caminho = os.path.join(self.diretorio_cache, arquivo)
                    
                    # Verificar idade
                    data_mod = datetime.fromtimestamp(os.path.getmtime(caminho))
                    idade = (datetime.now() - data_mod).days
                    
                    if idade > max_idade_dias:
                        os.remove(caminho)
                        limpos += 1
        except Exception:
            pass
        
        return limpos
    
    def on_documento_processado(self, callback: Callable):
        """Registrar callback para quando documento é processado"""
        self._on_documento_processado.append(callback)
    
    def on_erro_processamento(self, callback: Callable):
        """Registrar callback para quando há erro no processamento"""
        self._on_erro_processamento.append(callback)
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de leitura de PDFs"""
        return {
            "nome": self.nome,
            "versao": self.versao,
            "documentos_processados": len(self.documentos),
            "em_cache": len(self.cache_documentos),
            "total_pdfs": self.total_pdfs_processados,
            "total_paginas": self.total_paginas_processadas,
            "total_downloads": self.total_downloads,
            "erros": self.erros_processamento,
            "bibliotecas_disponiveis": {
                "pdfplumber": PDFPLUMBER_AVAILABLE,
                "pymupdf": Fitz_AVAILABLE,
                "pypdf2": PYPDF2_AVAILABLE,
                "requests": REQUESTS_AVAILABLE,
                "ocr": PYTESSERACT_AVAILABLE and PILLOW_AVAILABLE
            },
            "cache": self.diretorio_cache,
            "historico_downloads": len(self.historico_downloads)
        }


# ============== FUNÇÕES UTILITÁRIAS ==============

def extrair_texto_simples(caminho_pdf: str) -> str:
    """Extrair texto de PDF de forma simples (função standalone)"""
    try:
        if Fitz_AVAILABLE and fitz is not None:
            doc = fitz.open(caminho_pdf)
            texto = ""
            for page in doc:
                texto += page.get_text()
            doc.close()
            return texto
        
        elif PDFPLUMBER_AVAILABLE and pdfplumber is not None:
            with pdfplumber.open(caminho_pdf) as pdf:
                return "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        
        elif PYPDF2_AVAILABLE and PyPDF2 is not None:
            with open(caminho_pdf, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return "\n\n".join(page.extract_text() or "" for page in reader.pages)
    
    except Exception:
        pass
    
    return ""


def baixar_e_extrair(url: str, timeout: int = 30) -> Optional[str]:
    """Baixar PDF de URL e extrair texto"""
    if not REQUESTS_AVAILABLE or requests is None:
        return None
    
    try:
        # Download
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        # Salvar temporariamente
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
            tmp.write(response.content)
            tmp_path = tmp.name
        
        # Extrair texto
        texto = extrair_texto_simples(tmp_path)
        
        # Limpar
        os.unlink(tmp_path)
        
        return texto
        
    except Exception:
        return None
