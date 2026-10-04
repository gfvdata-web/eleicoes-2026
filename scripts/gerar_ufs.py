"""
Gera os arquivos estáticos de cada estado para es.html (rode uma vez; só biblioteca padrão):
  docs/data/uf/<uf>/municipios.json    [{tse, ibge, nome, micro, macro}]
  docs/data/uf/<uf>/municipios.geojson malha do IBGE (propriedade "ibge")

Códigos TSE e IBGE: config de municípios do TSE. Nomes, microrregião e mesorregião: IBGE.
O Espírito Santo continua em docs/data/es/ (regiões de planejamento do estado).

Uso: python scripts/gerar_ufs.py [UF ...]   (sem argumentos: todos, menos ES)
"""

import json
import sys
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TSE = "https://resultados.tse.jus.br/oficial/ele2026/6259/config/mun-e006259-cm.json"
IBGE = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
MALHA = "https://servicodados.ibge.gov.br/api/v3/malhas/estados/{uf}?intrarregiao=municipio&qualidade=minima&formato=application/vnd.geo+json"
UFS = "AC AL AP AM BA CE DF GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()


def baixar(url):
    req = urllib.request.Request(url, headers={"Accept-Encoding": "identity", "User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        dado = r.read()
    if dado[:2] == bytes([0x1F, 0x8B]):
        import gzip
        dado = gzip.decompress(dado)
    return dado


def arredondar(c, casas=3):
    return [arredondar(x, casas) for x in c] if isinstance(c[0], list) else [round(c[0], casas), round(c[1], casas)]


def main():
    alvo = [u.upper() for u in sys.argv[1:]] or UFS
    tse = json.loads(baixar(TSE).decode("utf-8"))
    por_uf = {x["cd"].upper(): x["mu"] for x in tse["abr"]}
    for uf in alvo:
        ibge = {str(m["id"]): m for m in json.loads(baixar(IBGE.format(uf=uf)))}
        muns = []
        for m in por_uf[uf]:
            i = ibge.get(m["cdi"])
            if not i:
                print(f"{uf}: {m['nm']} ({m['cdi']}) fora da lista do IBGE")
                continue
            micro = i["microrregiao"]
            if micro:
                reg, grande = micro["nome"], micro["mesorregiao"]["nome"]
            else:  # município novo, sem microrregião no IBGE: usa a região imediata/intermediária
                reg, grande = i["regiao-imediata"]["nome"], i["regiao-imediata"]["regiao-intermediaria"]["nome"]
            muns.append({"tse": m["cd"], "ibge": m["cdi"], "nome": i["nome"], "micro": reg, "macro": grande})
        muns.sort(key=lambda x: x["nome"])
        geo = json.loads(baixar(MALHA.format(uf=uf)).decode("utf-8"))
        for f in geo["features"]:
            f["properties"] = {"ibge": f["properties"]["codarea"]}
            f["geometry"]["coordinates"] = arredondar(f["geometry"]["coordinates"])
        pasta = RAIZ / "docs" / "data" / "uf" / uf.lower()
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "municipios.json").write_text(json.dumps(muns, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        (pasta / "municipios.geojson").write_text(json.dumps(geo, separators=(",", ":")) + "\n", encoding="utf-8")
        print(f"{uf}: {len(muns)} municípios, malha {(pasta / 'municipios.geojson').stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
