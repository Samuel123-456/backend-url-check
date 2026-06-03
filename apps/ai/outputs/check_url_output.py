from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class VetoresRisco(BaseModel):
    protocolo_seguro: bool = Field(
        ..., description="Indica se o link utiliza HTTPS (True) ou HTTP (False)"
    )
    dominio_oficial_reconhecido: bool = Field(
        ..., description="True se o domínio pertence comprovadamente a uma instituição legítima"
    )
    contem_typosquatting: bool = Field(
        ..., description="True se o link tenta imitar um nome real com erros ortográficos (ex: bancoba1)"
    )
    usa_encurtador: bool = Field(
        ..., description="True se a URL utiliza serviços como bit.ly, tinyurl, t.co, etc."
    )


class DetalheAnalise(BaseModel):
    componente: Literal["protocolo", "dominio", "texto_contextual", "encurtador"] = Field(
        ..., description="O componente da URL ou do contexto que foi analisado"
    )
    constatacao: str = Field(
        ..., description="O achado ou evidência encontrada na análise deste componente"
    )
    impacto_no_risco: Literal["alto", "medio", "baixo"] = Field(
        ..., description="O peso ou impacto deste componente no cálculo de risco total"
    )
    justificativa_tecnica: str = Field(
        ..., description="Explicação técnica detalhada do perigo ou da segurança detectada"
    )


class LinkAnalysisOutput(BaseModel):
    url_analisada: str = Field(
        ..., description="A URL completa que foi submetida para análise"
    )
    dominio_principal: str = Field(
        ..., description="O domínio base extraído da URL (ex: exemplo.com)"
    )
    classificacao_seguranca: Literal["seguro", "suspeito", "altamente_perigoso"] = Field(
        ..., description="Classificação final do link após a avaliação heurística"
    )
    percentagem_risco_global: int = Field(
        ...,
        ge=0,
        le=100,
        description="Nota de risco calculada matematicamente de 0 (totalmente seguro) a 100 (golpe confirmado)"
    )
    tipo_de_golpe_provavel: Literal[
        "phishing_bancario",
        "fraude_multicaixa_express",
        "falsa_vaga_emprego",
        "falsa_promocao_recarga",
        "malware_distribuicao",
        "legitimo"
    ] = Field(
        ..., description="A categoria do golpe com base nos padrões mapeados no mercado angolano"
    )
    nivel_de_urgencia_identificado: Literal["critico", "alto", "medio", "baixo"] = Field(
        ..., description="O nível de imediatismo ou coação psicológica usada na abordagem"
    )
    vetores_de_risco: VetoresRisco = Field(
        ..., description="Flags booleanos estruturados sobre a anatomia do link"
    )
    resumo_alerta: str = Field(
        ..., description="Mensagem curta e de alto impacto ideal para exibição rápida em cards ou toasts"
    )
    detalhes_da_analise: List[DetalheAnalise] = Field(
        ..., description="Lista detalhada que decompõe os fatores avaliados pelo motor de IA"
    )
    gatilhos_de_engenharia_social: List[
        Literal["urgencia", "medo", "autoridade_falsa", "recompensa_financeira", "nenhum"]
    ] = Field(
        ..., description="Gatilhos psicológicos identificados no texto ou na proposta do link"
    )
    entidades_mimetizadas: List[str] = Field(
        ..., description="Lista de marcas ou instituições angolanas que o golpe tenta falsificar (ex: ['Banco BAI', 'EMIS'])"
    )
    recomendacao_imediata_usuario: str = Field(
        ..., description="Orientação imperativa em português de como o utilizador deve proceder com este link"
    )