# 🤝 Contributing to the SPECTRA Framework

Thank you for your interest in contributing to **SPECTRA**.
This framework is designed as a **self-governing digital ecosystem** — contributions are welcome, but must align with the **Doctrine of Selves** and the **7×7×7 lattice**.

---

## 🛠 Contribution Workflow

1. **Fork** the repository and create your feature branch:

   ```bash
   git checkout -b feature/your-feature

   ```bash

2. **Commit** changes with clear, conventional messages:

   ```Text

   feat(principles): add resilience buffer capability
   fix(tools): update generate_readme.py for multi-pillar support

   ```

3. **Open a Pull Request** and link it to an Issue if applicable.
   All PRs are reviewed for **Spectra alignment** (mononyms, structure, governance).

---

## ✅ Contribution Standards

- **Mononyms only** – all repo names, capabilities, and services must be single, canonical words.
- **Orthogonality** – no overlaps between domains or capabilities.
- **Purity** – YAML is always the canonical source; Markdown is generated.
- **Compliance** – all workflows must pass CI/CD, linting, and security scans.

---

## 📖 Documentation

- Do not edit pillar `README.md` files directly.
- Update the corresponding `*.yaml` under `framework/principles/<pillar>/`.
- Run:

  ```bash
  python framework/tools/generate_readme.py framework/principles/<pillar>/<pillar>.yaml

  ```

  to regenerate the human-readable docs.

---

## 🛡️ Code of Conduct

We adhere to a strict **zero-toxicity policy**:

- Respect all contributors.
- Critique ideas, not people.
- No harassment, discrimination, or hostility.

---

## 🏆 Recognition

Every merged contribution is part of the **SPECTRA self-evolution**.
You are shaping a living system that grows smarter with every commit.

Thank you for helping **Spectrafy** the ecosystem! 🌟
