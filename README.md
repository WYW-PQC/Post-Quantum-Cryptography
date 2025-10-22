# Defence Post-Quantum Cryptography (PQC) Implementation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A production-grade implementation of NIST-selected Post-Quantum Cryptography algorithms for defence and governmental infrastructure.

## 🎯 Project Overview

This project implements quantum-resistant cryptographic algorithms selected by NIST, focusing on:
- **ML-KEM (CRYSTALS-Kyber)** - Primary Key Encapsulation Mechanism
- **ML-DSA (CRYSTALS-Dilithium)** - Primary Digital Signature Algorithm
- **FALCON** - High-performance signature alternative
- **SPHINCS+** - Hash-based signature for diversification

## 📋 Current Status

**Phase 1: Foundation Building (2025-2026)**
- [x] Project initialization
- [ ] Standards review (Q3-Q4 2025)
- [ ] Algorithm selection documentation (Q4 2025)
- [ ] Environment setup (Q4 2025 - Q1 2026)
- [ ] Initial implementation (Q1-Q3 2026)

## 🚀 Quick Start

### Prerequisites

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install cmake gcc ninja-build libssl-dev python3-pip

# macOS
brew install cmake ninja openssl python3
```

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/defence-pqc.git
cd defence-pqc

# Install Python dependencies
pip install -r requirements.txt

# Build liboqs (automated script)
./scripts/setup_liboqs.sh

# Run initial tests
python -m pytest tests/
```

### Docker Setup (Recommended)

```bash
docker build -t defence-pqc .
docker run -it defence-pqc bash
```

## 📁 Repository Structure

```
defence-pqc/
├── src/
│   ├── kem/              # Key Encapsulation Mechanisms
│   │   ├── kyber.py
│   │   └── __init__.py
│   ├── signatures/       # Digital Signatures
│   │   ├── dilithium.py
│   │   ├── falcon.py
│   │   ├── sphincs.py
│   │   └── __init__.py
│   ├── hybrid/           # Hybrid classical+PQC protocols
│   │   └── tls_hybrid.py
│   └── utils/            # Utilities and benchmarking
│       ├── benchmark.py
│       └── crypto_utils.py
├── tests/
│   ├── test_kem.py
│   ├── test_signatures.py
│   └── test_benchmarks.py
├── benchmarks/           # Performance measurement suites
├── docs/
│   ├── algorithm_selection.md
│   ├── security_analysis.md
│   └── deployment_guide.md
├── scripts/
│   ├── setup_liboqs.sh
│   └── run_benchmarks.sh
├── docker/
│   └── Dockerfile
├── requirements.txt
├── setup.py
└── README.md
```

## 🔧 Implementation Details

### Supported Algorithms

| Algorithm | Type | Status | NIST Standard |
|-----------|------|--------|---------------|
| ML-KEM (Kyber) | KEM | ✅ Implemented | FIPS 203 |
| ML-DSA (Dilithium) | Signature | ✅ Implemented | FIPS 204 |
| FALCON | Signature | 🚧 In Progress | FIPS 206 |
| SPHINCS+ | Signature | 📋 Planned | FIPS 205 |

### Parameter Sets

- **Kyber-512, Kyber-768, Kyber-1024** (AES-128, AES-192, AES-256 equivalent)
- **Dilithium-2, Dilithium-3, Dilithium-5**
- **FALCON-512, FALCON-1024**
- **SPHINCS+-128s, SPHINCS+-256s**

## 📊 Benchmarking

Run comprehensive benchmarks:

```bash
python -m src.utils.benchmark --algorithms kyber,dilithium --iterations 1000
```

Expected metrics:
- Key generation time (ms)
- Encapsulation/Decapsulation latency (μs)
- Signature generation/verification time (ms)
- Memory footprint (KB)

## 🔒 Security Considerations

- All implementations use constant-time operations where applicable
- Side-channel resistance measurements included
- Regular security audits planned (Phase 2)
- Formal verification targets documented in `docs/security_analysis.md`

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📚 Documentation

- [Algorithm Selection Rationale](docs/algorithm_selection.md)
- [Security Analysis](docs/security_analysis.md)
- [Deployment Guide](docs/deployment_guide.md)
- [API Reference](docs/api_reference.md)

## 🗺️ Roadmap

### Phase 1: Foundation (2025-2026)
- Standards review and algorithm selection
- Initial implementation of ML-KEM and ML-DSA
- Benchmark suite development
- White paper publication

### Phase 2: Development & Testing (2027-2028)
- Hybrid TLS prototype
- Quantum simulation testing
- Performance optimization
- Pilot deployment

### Phase 3: Production Deployment (2029-2030)
- Production hardening
- Industry interoperability
- Open-source release
- Impact assessment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 References

- [NIST PQC Project](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Open Quantum Safe](https://openquantumsafe.org/)
- [liboqs Documentation](https://github.com/open-quantum-safe/liboqs)
- [CRYSTALS Suite](https://pq-crystals.org/)

## 👥 Team & Contact

Defence Cryptography Research Team
- Email: pqc-team@defence.gov
- Issue Tracker: [GitHub Issues](https://github.com/your-org/defence-pqc/issues)

## 🙏 Acknowledgments

- NIST for the PQC standardization process
- Open Quantum Safe project contributors
- CRYSTALS team for algorithm development

---

**⚠️ Security Notice**: This is research/development code. Do not use in production environments without thorough security review and testing.
