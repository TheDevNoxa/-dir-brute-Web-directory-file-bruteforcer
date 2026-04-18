# 📂 dir-brute

Outil de découverte de répertoires et fichiers web — projet éducatif réalisé dans le cadre du Bac Pro CIEL.

## Fonctionnalités

- Bruteforce de chemins web avec wordlist personnalisable
- Support d'extensions multiples (`.php`, `.html`, `.bak`…)
- Multi-threadé avec délai configurable
- Détecte les 200 (trouvé), 403/401 (interdit mais existant), redirections
- Wordlist intégrée de 50+ chemins communs

## Installation

```bash
git clone https://github.com/thedevnoxa/dir-brute
cd dir-brute
# Aucune dépendance externe
```

## Utilisation

```bash
# Avec wordlist intégrée
python3 dir_brute.py -u https://example.com

# Avec wordlist externe et extensions
python3 dir_brute.py -u https://example.com -w /usr/share/wordlists/dirb/common.txt -x .php,.html

# Sans extensions, plus de threads
python3 dir_brute.py -u https://example.com --no-ext --threads 50

# Avec délai (pour éviter de surcharger)
python3 dir_brute.py -u https://example.com --delay 0.5
```

## Exemple de sortie

```
[*] Target    : https://example.com
[*] Words     : 50
[*] Extensions: ['', '.php', '.html', '.txt']
[*] Total URLs: 200

[200]  https://example.com/robots.txt                            142b
[200]  https://example.com/sitemap.xml                           3201b
[403]  https://example.com/admin
[403]  https://example.com/backup
[200]  https://example.com/readme.html                           8432b

=================================================================
  RESULTS — 5 path(s) found
=================================================================
  [200]  https://example.com/robots.txt
  [200]  https://example.com/sitemap.xml
  [200]  https://example.com/readme.html
  [403]  https://example.com/admin
  [403]  https://example.com/backup
=================================================================
```

## ⚠️ Avertissement légal

Usage **éducatif uniquement**. Testez uniquement des serveurs dont vous êtes responsable ou avec autorisation écrite. Des environnements légaux pour s'entraîner : [DVWA](https://dvwa.co.uk/), [HackTheBox](https://hackthebox.com), [TryHackMe](https://tryhackme.com).

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

---
*Projet réalisé par [Noxa](https://github.com/thedevnoxa) — Bac Pro CIEL*
