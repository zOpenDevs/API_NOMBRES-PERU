import requests

AJAX_URL = "https://dniperu.com/wp-admin/admin-ajax.php"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Origin": "https://dniperu.com",
    "Referer": "https://dniperu.com/buscar-dni-por-nombre/",
}


def get_token(session, context="buscar_dni"):
    data = {
        "action": "cc_get_tokens",
        "context": context,
        "company": "",
        "count": "1",
    }
    resp = session.post(AJAX_URL, data=data, headers=HEADERS)
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("success") or not payload.get("data"):
        raise Exception("No se pudo obtener token")
    tokens = payload["data"].get("tokens", [])
    if tokens:
        return tokens[0]
    return {
        "cc_token": payload["data"]["cc_token"],
        "cc_sig": payload["data"]["cc_sig"],
    }


def buscar_dni(session, nombres, apellido_paterno, apellido_materno):
    data = {
        "action": "buscar_dni",
        "nombres": nombres,
        "apellido_paterno": apellido_paterno,
        "apellido_materno": apellido_materno,
        "company": "",
    }
    resp = session.post(AJAX_URL, data=data, headers=HEADERS)
    resp.raise_for_status()
    result = resp.json()
    if (
        isinstance(result, dict)
        and result.get("data", {}).get("code") == "token_required"
    ):
        token = get_token(session)
        data["cc_token"] = token["cc_token"]
        data["cc_sig"] = token["cc_sig"]
        resp = session.post(AJAX_URL, data=data, headers=HEADERS)
        resp.raise_for_status()
        result = resp.json()
    return result


def formatear_resultados(resultados):
    output = []
    for p in resultados["data"]["resultados"]:
        output.append({
            "od_nombres": p["nombres"],
            "od_apaterno": p["apellido_paterno"],
            "od_amaterno": p["apellido_materno"],
            "od_dni": p["numero"],
        })
    return output
