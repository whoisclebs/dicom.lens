<div align="center">
  <h1>DicomLens</h1>
  <p><strong>Open‑source platform</strong> for medical image analysis and cancer detection</p>
</div>

<p align="center">
  <a href="https://github.com/whoisclebs/dicom.lens/blob/main/LICENSE"><img src="https://img.shields.io/github/license/whoisclebs/dicom.lens" alt="License"/></a>
  <a href="https://github.com/whoisclebs/dicom.lens/actions"><img src="https://img.shields.io/github/actions/workflow/status/whoisclebs/dicom.lens/codeql.yml" alt="CI Status"/></a>
  <a href="https://dicomlens.whoisclebs.com"><img src="https://img.shields.io/badge/docs-live-blue" alt="Documentation"/></a>
</p>

---

## Table of Contents
- [About](#about)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Training a Model](#training-a-model)
  - [Exploration Notebook](#exploration-notebook)
  - [API & Frontend](#api--frontend)
- [Contributing](#contributing)
- [License](#license)

---

## About
DicomLens is an open‑source framework for analyzing DICOM medical images using machine learning. Initially focused on breast cancer detection, its modular design supports extension to multiple imaging tasks and seamless integration between training, exploration, and deployment.

## Features
- Binary classification of scans (e.g., healthy vs. cancer)
- **Modular CLI**: `train.py` for production‑ready training
- **Exploration Notebook**: interactive prototyping with Jupyter
- **Web API**: Node.js backend under `web/api` for serving predictions
- **Frontend**: React/Vite dashboard under `web/front`
- **CI/CD**: Automated model training and API deployment workflows

## Architecture

```
├── .github/               # GitHub Actions & workflows
├── .husky/                # Git hooks
├── ml/
│   ├── data/              # (gitignored) raw DICOM dataset
│   ├── notebooks/         # Jupyter notebooks (exploration.ipynb)
│   ├── scripts/           # CLI scripts:
│   │   ├── fetch_data.sh  # pulls DICOMs from external storage
│   │   └── train.py       # training entrypoint
│   └── models/            # (gitignored) trained artifacts
├── packages/              # shared libraries/modules
├── web/
│   ├── api/               # Node.js prediction API
│   └── front/             # React/Vite frontend dashboard
├── CODE_OF_CONDUCT.md     # Contribution guidelines
├── CONTRIBUTING.md        # How to contribute
├── CITATION.cff           # Citation metadata
├── LICENSE                # MIT License
└── README.md              # Project overview (this file)
```

## Getting Started

### Prerequisites
- **Python 3.8+** (and `pip`)
- **Node.js 16+** (and `npm`)
- (Optional) **Docker** & **Docker Compose**

### Installation

1. **Clone the repo**
    ```bash
    git clone https://github.com/yourusername/dicom.lens.git
    cd dicomlens
    ```

2. **Python setup**
    ```bash
    cd ml
    python -m venv venv
    source venv/bin/activate
    pip install -r scripts/requirements.txt
    ```

3. **Node.js setup**
    ```bash
    cd ../web/api
    npm install
    ```

4. **Frontend setup**
    ```bash
    cd ../front
    npm install
    ```

5. **Data ingestion**
    ```bash
    cd ../../ml/scripts
    ./fetch_data.sh   # pulls raw DICOMs into ../data/
    ```

## Usage

### Training a Model
Run the CLI to train and save a model:
```bash
cd ml/scripts
python train.py \
  --data-dir ../data \
  --output ../models/v1 \
  --img-size 224 224 \
  --batch-size 32 \
  --epochs 20
```
Artifacts (best_model.h5, SavedModel) appear under `ml/models/v1/`.

### Exploration Notebook
For interactive prototyping:
```bash
cd ml/notebooks
jupyter notebook exploration.ipynb
```
Use this to visualize samples, tune augmentations, and inspect metrics.

### API & Frontend
1. **Configure API**: in `web/api/.env`, set:
    ```env
    MODEL_URL=https://storage.example.com/models/v1/model.json
    ```
2. **Start API**:
    ```bash
    cd web/api
    npm start
    ```
3. **Start Frontend**:
    ```bash
    cd web/front
    npm run dev
    ```
Visit the dashboard (default http://localhost:3000).

## Contributing
We welcome contributions! Please:
1. Fork the repo
2. Create a branch (`feature/xxx`)
3. Submit a PR with tests/docs

See [`CONTRIBUTING.md`](CONTRIBUTING.md) and our [Code of Conduct](CODE_OF_CONDUCT.md).

## License
This project is released under the MIT License. See [`LICENSE`](LICENSE) for details.