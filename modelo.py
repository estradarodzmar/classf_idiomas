import math
import re
from collections import Counter

# -------------------------
# Datos de entrenamiento
# -------------------------
TRAIN_DATA = {
    "ESPAÑOL": "hola gracias amigo casa día amor comida mañana sol familia",
    "INGLES": "hello thank friend house day love food morning sun family",
    "FRANCES": "bonjour merci ami maison jour amour nourriture matin soleil famille"
}

TOKEN_RE = re.compile(r"[a-zA-Záéíóúüñçàâêîôûèëïÿœ'-]+", re.UNICODE)

def tokenize(text):
    return TOKEN_RE.findall(text.lower())

def entrenar(data):
    modelos = {}
    vocabulario = set()
    total_palabras = {}

    for idioma, texto in data.items():
        tokens = tokenize(texto)
        conteo = Counter(tokens)
        modelos[idioma] = conteo
        total_palabras[idioma] = sum(conteo.values())
        vocabulario.update(tokens)

    return modelos, vocabulario, total_palabras

modelos, vocabulario, total_palabras = entrenar(TRAIN_DATA)
alpha = 1.0  # suavizado

def p_palabra_dado_idioma(palabra, idioma):
    V = len(vocabulario)
    count = modelos[idioma][palabra]
    return (count + alpha) / (total_palabras[idioma] + alpha * V)

def clasificador(texto):
    tokens = tokenize(texto)
    if not tokens:
        return {"error": "No se detectaron palabras."}

    idiomas = list(TRAIN_DATA.keys())
    priors = {idioma: 1/len(idiomas) for idioma in idiomas}
    log_probs = {}

    for idioma in idiomas:
        logp = math.log(priors[idioma])
        for token in tokens:
            logp += math.log(p_palabra_dado_idioma(token, idioma))
        log_probs[idioma] = logp

    max_log = max(log_probs.values())
    exp_probs = {idioma: math.exp(v - max_log) for idioma, v in log_probs.items()}
    total = sum(exp_probs.values())
    probs = {idioma: exp_probs[idioma] / total for idioma in idiomas}
    predicho = max(probs, key=probs.get)

    return {
        "texto": texto,
        "predicted": predicho,
        "probabilities": probs
    }
