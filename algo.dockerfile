# Defence Post-Quantum Cryptography - Docker Environment
# Multi-stage build for optimized image size

FROM ubuntu:22.04 as builder

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV LIBOQS_VERSION=0.10.1
ENV OQS_OPENSSL_VERSION=111

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    ninja-build \
    libssl-dev \
    python3 \
    python3-pip \
    python3-dev \
    wget \
    unzip \
    astyle \
    && rm -rf /var/lib/apt/lists/*

# Build liboqs from source
WORKDIR /build
RUN git clone --depth 1 --branch ${LIBOQS_VERSION} https://github.com/open-quantum-safe/liboqs.git && \
    cd liboqs && \
    mkdir build && cd build && \
    cmake -GNinja \
    -DCMAKE_INSTALL_PREFIX=/opt/liboqs \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=ON \
    -DOQS_BUILD_ONLY_LIB=OFF \
    .. && \
    ninja && \
    ninja install

# Build liboqs-python
WORKDIR /build
RUN git clone --depth 1 https://github.com/open-quantum-safe/liboqs-python.git && \
    cd liboqs-python && \
    pip3 install --no-cache-dir .

# Production stage
FROM ubuntu:22.04

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Copy liboqs from builder
COPY --from=builder /opt/liboqs /opt/liboqs

# Set library path
ENV LD_LIBRARY_PATH=/opt/liboqs/lib:$LD_LIBRARY_PATH
ENV PATH=/opt/liboqs/bin:$PATH

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY tests/ ./tests/
COPY scripts/ ./scripts/
COPY benchmarks/ ./benchmarks/

# Create directories for outputs
RUN mkdir -p /app/outputs /app/logs

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Run tests on build to verify setup
RUN python3 -c "import oqs; print('liboqs version:', oqs.oqs_version())"

# Default command
CMD ["/bin/bash"]