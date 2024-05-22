# test_wallet


### Prerequisites

What things you need to install the software and how to install them:

- Docker
- Docker Compose

You can download Docker Desktop for Mac or Windows, which includes Docker Compose, from [Docker Hub](https://hub.docker.com/).

### Installing

A step-by-step series of examples that tell you how to get a development environment running:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Sibuken/test_wallet.git
   cd test_wallet
   ```

2. **Build Docker image**

   ```bash
   docker compose build
   ```

3. **Start the application**

   ```bash
    docker compose up
    ```

4. **Run the tests**

   ```bash
   docker compose run --rm web python -m pytest .
   ```
