#!/usr/bin/env python3
import os
import subprocess
import urllib.request
import time

SERVER_DIR = "/opt/minecraft"
RAM = "16G"

PAPER_URL = "https://fill-data.papermc.io/v1/objects/b727f13945dd442cd2bc1de6c64680e8630e7f54ba259aac7687e9c7c3cc18a3/paper-1.21.11-97.jar"

# Plugins dictionary: filename -> download URL
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

def main():
    # Install Java
    run("apt update")
    run("apt install -y openjdk-21-jdk wget")

    # Create directories
    plugins_dir = f"{SERVER_DIR}/plugins"
    os.makedirs(plugins_dir, exist_ok=True)

    # Download Paper
    print("Downloading Paper 1.21.11...")
    urllib.request.urlretrieve(PAPER_URL, f"{SERVER_DIR}/paper.jar")

    # Accept EULA
    with open(f"{SERVER_DIR}/eula.txt", "w") as f:
        f.write("eula=true\n")

    # Download all plugins
    print("Downloading plugins...")
    for name, url in PLUGINS.items():
        print(f" - {name}")
        urllib.request.urlretrieve(url, f"{plugins_dir}/{name}")

    # Start server
    print("Starting Minecraft server...")
    os.chdir(SERVER_DIR)
    server = subprocess.Popen(
        [
            "java",
            f"-Xms{RAM}",
            f"-Xmx{RAM}",
            "-jar",
            "paper.jar",
            "nogui"
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # Wait for server startup
    print("Waiting for server to fully start...")
    time.sleep(30)

    # OP the player
    print("Granting OP to bankrollsnblunts...")
    server.stdin.write("op bankrollsnblunts\n")
    server.stdin.flush()

    # Stream console output
    for line in server.stdout:
        print(line, end="")

if __name__ == "__main__":
    main()
