# Good First Issues pour Open Cyber Lab

Voici des suggestions d'issues à créer sur GitHub pour attirer des contributeurs:

---

## 🚀 Feature: Ajouter des tests pour les labs existants

**Description:** Ajouter des tests unitaires pour les 17 labs existants.

**Lab:** `tests/test_labs.py`

**Exemples de tests à ajouter:**
- Tester que chaque lab a une fonction `run()`
- Tester que chaque lab a les métadonnées (`DIFFICULTY`, `OBJECTIVES`)
- Tester les cas limites

**Difficulté:** Beginner

---

## 🚀 Feature: Améliorer le système de progression

**Description:** Le système de progression actuel est basique. Ajouter:
- Score par lab
- Temps passé sur chaque lab
- Badges/achievements
- Tableau de classement

**Fichiers:** `cyberlab/progress.py`

**Difficulté:** Intermediate

---

## 🚀 Feature: Ajouter un système de hints

**Description:** Les learners peuvent avoir besoin d'aide. Ajouter:
- Commande `hint` pour chaque lab
- Limite de hints par lab
- Points déduits pour l'utilisation de hints

**Fichiers:** `cyberlab/cli.py`, `labs/*.py`

**Difficulté:** Intermediate

---

## 🐛 Bug: Corriger les tests sur Windows

**Description:** Certains tests échouent sur Windows à cause de:
- Problèmes de permissions sur les fichiers temporaires
- Chemins de fichiers

**Fichiers:** `tests/test_progress.py`

**Difficulté:** Beginner

---

## 📚 Documentation: Améliorer le README

**Description:** Le README peut être amélioré avec:
- Plus d'exemples d'utilisation
- Screenshots
- Diagramme d'architecture
- Badges CI/CD

**Fichier:** `README.md`

**Difficulté:** Beginner

---

## 🧪 Nouveau Lab: Phishing Awareness

**Description:** Créer un lab pour apprendre à détecter les emails de phishing.

**Objectifs:**
- Identifier les signes d'un email de phishing
- Analyser les URLs suspectes
- Comprendre les techniques de social engineering

**Difficulté:** Beginner

---

## 🧪 Nouveau Lab: Social Engineering

**Description:** Simuler des scénarios de social engineering.

**Objectifs:**
- Reconnaître les tentatives de manipulation
- Apprendre les techniques d'ingénierie sociale
- Protéger les informations sensibles

**Difficulté:** Intermediate

---

## 🎨 Amélioration CLI: Couleurs et formatting

**Description:** Améliorer l'interface CLI avec:
- Plus de couleurs (status, warnings, errors)
- Progress bars
- Tableaux mieux formatés
- Animation de chargement

**Fichiers:** `cyberlab/cli.py`

**Difficulté:** Beginner

---

## 🔧 CI/CD: Ajouter coverage reporting

**Description:** Configurer GitHub Actions pour:
- Rapports de coverage avec Codecov ou Coveralls
- Badges de coverage dans le README
- Déclencher des alerts si coverage baisse

**Fichiers:** `.github/workflows/ci.yml`

**Difficulté:** Intermediate

---

## 💡 Suggestion: Ajouter un mode "Challenge"

**Description:** Un mode où les utilisateurs peuvent:
- Combiner plusieurs vulnérabilités
- Résoudre des scénarios complexes
- Gagner des points bonus

**Difficulté:** Advanced
