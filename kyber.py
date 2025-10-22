"""
ML-KEM (CRYSTALS-Kyber) Implementation Wrapper
Post-Quantum Key Encapsulation Mechanism

This module provides a Python interface to liboqs Kyber implementation
with additional utilities for benchmarking and security analysis.
"""

import time
import json
from typing import Tuple, Dict, Optional
from dataclasses import dataclass
import logging

try:
    import oqs
except ImportError:
    oqs = None
    logging.warning("liboqs not installed. Install with: pip install liboqs-python")


@dataclass
class KyberParameters:
    """Parameter sets for Kyber variants"""
    name: str
    security_level: int  # AES equivalent (128, 192, 256)
    public_key_bytes: int
    secret_key_bytes: int
    ciphertext_bytes: int
    shared_secret_bytes: int


KYBER_PARAMS = {
    "Kyber512": KyberParameters(
        name="Kyber512",
        security_level=128,
        public_key_bytes=800,
        secret_key_bytes=1632,
        ciphertext_bytes=768,
        shared_secret_bytes=32
    ),
    "Kyber768": KyberParameters(
        name="Kyber768",
        security_level=192,
        public_key_bytes=1184,
        secret_key_bytes=2400,
        ciphertext_bytes=1088,
        shared_secret_bytes=32
    ),
    "Kyber1024": KyberParameters(
        name="Kyber1024",
        security_level=256,
        public_key_bytes=1568,
        secret_key_bytes=3168,
        ciphertext_bytes=1568,
        shared_secret_bytes=32
    )
}


class KyberKEM:
    """
    CRYSTALS-Kyber Key Encapsulation Mechanism
    
    Provides quantum-resistant key establishment using lattice-based cryptography.
    Supports Kyber512, Kyber768, and Kyber1024 parameter sets.
    """
    
    def __init__(self, variant: str = "Kyber768"):
        """
        Initialize Kyber KEM with specified variant
        
        Args:
            variant: One of "Kyber512", "Kyber768", "Kyber1024"
        """
        if variant not in KYBER_PARAMS:
            raise ValueError(f"Invalid variant. Choose from {list(KYBER_PARAMS.keys())}")
        
        self.variant = variant
        self.params = KYBER_PARAMS[variant]
        
        if oqs is None:
            raise RuntimeError("liboqs-python not available. Cannot initialize Kyber.")
        
        self.kem = oqs.KeyEncapsulation(variant)
        self.logger = logging.getLogger(__name__)
        
    def generate_keypair(self) -> Tuple[bytes, bytes]:
        """
        Generate a new Kyber keypair
        
        Returns:
            Tuple of (public_key, secret_key)
        """
        start_time = time.perf_counter()
        public_key = self.kem.generate_keypair()
        secret_key = self.kem.export_secret_key()
        elapsed = time.perf_counter() - start_time
        
        self.logger.debug(f"Keypair generation took {elapsed*1000:.3f}ms")
        
        return public_key, secret_key
    
    def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]:
        """
        Encapsulate a shared secret using recipient's public key
        
        Args:
            public_key: Recipient's public key
            
        Returns:
            Tuple of (ciphertext, shared_secret)
        """
        start_time = time.perf_counter()
        ciphertext, shared_secret = self.kem.encap_secret(public_key)
        elapsed = time.perf_counter() - start_time
        
        self.logger.debug(f"Encapsulation took {elapsed*1000:.3f}ms")
        
        return ciphertext, shared_secret
    
    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes:
        """
        Decapsulate shared secret using secret key
        
        Args:
            ciphertext: Encapsulated ciphertext
            secret_key: Recipient's secret key
            
        Returns:
            Shared secret
        """
        start_time = time.perf_counter()
        shared_secret = self.kem.decap_secret(ciphertext)
        elapsed = time.perf_counter() - start_time
        
        self.logger.debug(f"Decapsulation took {elapsed*1000:.3f}ms")
        
        return shared_secret
    
    def get_algorithm_info(self) -> Dict:
        """Get algorithm parameters and capabilities"""
        return {
            "algorithm": "ML-KEM (CRYSTALS-Kyber)",
            "variant": self.variant,
            "nist_level": self.params.security_level,
            "public_key_size": self.params.public_key_bytes,
            "secret_key_size": self.params.secret_key_bytes,
            "ciphertext_size": self.params.ciphertext_bytes,
            "shared_secret_size": self.params.shared_secret_bytes,
            "claimed_nist_level": self.kem.details.get('claimed_nist_level'),
            "version": self.kem.details.get('version', 'unknown')
        }
    
    def benchmark(self, iterations: int = 1000) -> Dict:
        """
        Run performance benchmarks
        
        Args:
            iterations: Number of operations to perform
            
        Returns:
            Dictionary with timing statistics
        """
        keygen_times = []
        encap_times = []
        decap_times = []
        
        for _ in range(iterations):
            # Key generation
            start = time.perf_counter()
            pk, sk = self.generate_keypair()
            keygen_times.append(time.perf_counter() - start)
            
            # Encapsulation
            start = time.perf_counter()
            ct, ss_enc = self.encapsulate(pk)
            encap_times.append(time.perf_counter() - start)
            
            # Decapsulation
            start = time.perf_counter()
            ss_dec = self.decapsulate(ct, sk)
            decap_times.append(time.perf_counter() - start)
            
            # Verify correctness
            assert ss_enc == ss_dec, "Shared secret mismatch!"
        
        return {
            "variant": self.variant,
            "iterations": iterations,
            "keygen_avg_ms": sum(keygen_times) / iterations * 1000,
            "keygen_min_ms": min(keygen_times) * 1000,
            "keygen_max_ms": max(keygen_times) * 1000,
            "encap_avg_ms": sum(encap_times) / iterations * 1000,
            "encap_min_ms": min(encap_times) * 1000,
            "encap_max_ms": max(encap_times) * 1000,
            "decap_avg_ms": sum(decap_times) / iterations * 1000,
            "decap_min_ms": min(decap_times) * 1000,
            "decap_max_ms": max(decap_times) * 1000
        }


def main():
    """Demo and testing"""
    logging.basicConfig(level=logging.INFO)
    
    print("=== CRYSTALS-Kyber KEM Demo ===\n")
    
    for variant in ["Kyber512", "Kyber768", "Kyber1024"]:
        print(f"\n--- {variant} ---")
        kem = KyberKEM(variant)
        
        # Show parameters
        info = kem.get_algorithm_info()
        print(f"Security Level: AES-{info['nist_level']}")
        print(f"Public Key: {info['public_key_size']} bytes")
        print(f"Ciphertext: {info['ciphertext_size']} bytes")
        
        # Quick benchmark
        print("\nRunning quick benchmark (100 iterations)...")
        results = kem.benchmark(iterations=100)
        print(f"KeyGen:  {results['keygen_avg_ms']:.3f}ms")
        print(f"Encap:   {results['encap_avg_ms']:.3f}ms")
        print(f"Decap:   {results['decap_avg_ms']:.3f}ms")


if __name__ == "__main__":
    main()