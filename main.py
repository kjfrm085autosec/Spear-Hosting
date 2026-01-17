#!/usr/bin/env python3
import os
import subprocess
import urllib.request

SERVER_DIR = "/opt/minecraft"
RAM = "4G"  # Adjust if needed

PAPER_URL = "https://fill-data.papermc.io/v1/objects/b727f13945dd442cd2bc1de6c64680e8630e7f54ba259aac7687e9c7c3cc18a3/paper-1.21.11-97.jar"

PLUGINS = {
    "EssentialsX.jar": "https://github.com/EssentialsX/Essentials/releases/download/2.21.2/EssentialsX-2.21.2.jar",
    "DiscordSRV.jar": "https://github.com/DiscordSRV/DiscordSRV/releases/download/v1.30.4/DiscordSRV-Build-1.30.4.jar",
    "ViaVersion.jar": "https://github.com/ViaVersion/ViaVersion/releases/download/5.7.0/ViaVersion-5.7.0.jar",
    "ViaRewind.jar": "https://github.com/ViaVersion/ViaRewind/releases/download/4.0.13/ViaRewind-4.0.13.jar",
    "WorldGuard.jar": "https://cdn.modrinth.com/data/DKY9btbd/versions/WaElxvDz/worldguard-bukkit-7.0.15.jar",
    "FastAsyncWorldEdit-Paper.jar": "https://cdn.modrinth.com/data/z4HZZnLr/versions/mHtmqIig/FastAsyncWorldEdit-Paper-2.15.0.jar",
    "ElytraVaults.jar": "https://cdn.modrinth.com/data/qvUvo44k/versions/EYbhEaCc/ElytraVaults-1.1.1.0.jar",
    "Grimac.jar": "https://cdn.modrinth.com/data/LJNGWSvH/versions/NxWPNaqP/grimac-bukkit-2.3.73-cd86c14.jar",
    "StringDupersReturn.jar": "https://cdn.modrinth.com/data/U6d1TJQm/versions/xTeVKr1m/StringDupersReturn-1.0.11.jar",
    "LPC-Minimessage.jar": "https://cdn.modrinth.com/data/LOlAU5yB/versions/gpoTpxDU/LPC-Minimessage.jar",
    "LuckPerms-Bukkit.jar": "https://cdn.modrinth.com/data/Vebnzrzj/versions/OrIs0S6b/LuckPerms-Bukkit-5.5.17.jar",
    "SmartSpawner.jar": "https://cdn.modrinth.com/data/9tQwxSFr/versions/QTPx8MMo/SmartSpawner-1.5.8.jar",
    "DonutSMPTools.jar": "https://cdn.modrinth.com/data/Zq9uFUif/versions/5Aug2eA1/DonutSMPTools-1.21.8-1.0.jar",
    "RulesGUI.jar": "https://cdn.modrinth.com/data/U8zaZwu5/versions/oyLGFewL/RulesGUI-1.0.0.jar",
    "RexonBaltop.jar": "https://cdn.modrinth.com/data/GcaR3xRS/versions/vTOHojht/RexonBaltop1.0.0.jar",
    "PlaceholderAPI.jar": "https://cdn.modrinth.com/data/lKEzGugV/versions/sn9LYZkM/PlaceholderAPI-2.11.7.jar",
    "Bounties.jar": "https://cdn.modrinth.com/data/oX7p9ZKO/versions/f3lgR3Mz/Bounties.jar",
    "RexonRTP.jar": "https://cdn.modrinth.com/data/vBP2HliW/versions/ZcGJXy6l/RexonRTP2.0.jar"
}

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def download_file(url, dest):
    """Download a file with proper User-Agent"""
    print(f"Downloading {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "minecraft-server-setup/1.0"})
    with urllib.request.urlopen(req) as response, open(dest, "wb") as out_file:
        out_file.write(response.read())
    print(f"Saved to {dest}")

def main():
    # Optional: Install Java if needed (requires sudo)
    # run("apt update")
    # run("apt install -y openjdk-21-jdk wget")

    # Create server directories
    plugins_dir = os.path.join(SERVER_DIR, "plugins")
    os.makedirs(plugins_dir, exist_ok=True)

    # Download Paper
    download_file(PAPER_URL, os.path.join(SERVER_DIR, "paper.jar"))

    # Accept EULA
    with open(os.path.join(SERVER_DIR, "eula.txt"), "w") as f:
        f.write("eula=true\n")

    # Download all plugins
    for name, url in PLUGINS.items():
        download_file(url, os.path.join(plugins_dir, name))

    # Ensure correct permissions (fixes session.lock issues)
    os.chmod(SERVER_DIR, 0o755)
    for root, dirs, files in os.walk(SERVER_DIR):
        for d in dirs:
            os.chmod(os.path.join(root, d), 0o755)
        for f in files:
            os.chmod(os.path.join(root, f), 0o644)

    # Start server
    os.chdir(SERVER_DIR)
    server = subprocess.Popen(
        ["java", f"-Xms2G", f"-Xmx{RAM}", "-jar", "paper.jar", "nogui"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Wait until server prints "Done"
    print("Waiting for server to fully start...")
    while True:
        line = server.stdout.readline()
        if not line:
            break
        print(line, end="")
        if "Done (" in line:
            server.stdin.write("op bankrollsnblunts\n")
            server.stdin.flush()
            print("Granted OP to bankrollsnblunts")

    # Stream remaining console output
    for line in server.stdout:
        print(line, end="")

if __name__ == "__main__":
    main()
