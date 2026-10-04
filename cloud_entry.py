import sys
import os

# Render dynamically assigns a port via an environment variable
# If it's missing, it defaults to port 10000
port = int(os.environ.get("PORT", 10000))
print(f"Starting Pycraft Server on port {port}...")

# Add your root pycraft directory to python's import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Attempting to load your networking server script directly
    from pycraft.net.server import main
    if __name__ == "__main__":
        main()
except ImportError:
    # Fallback structure if your code initializes via a class
    from pycraft.net.server import Server
    if __name__ == "__main__":
        server = Server(port=port)
        server.start()

