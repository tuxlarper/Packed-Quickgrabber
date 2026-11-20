import subprocess
import shutil
import platform
import os
# Under The Creative Commons ShareAlike 4.0 International License.
#Feel Free To ReDistrubute, Modify, And Share This Code. Just Give Credit To Me! @tuxlarper
#Orginal Github Repo: github.com/Tuxlarper/Packed-QuickGrabber
print("QuickGrabber Arch Pacman-Based Installer")
print("Developed By Tuxlarper And Fully Open Source. Made With Love")
print("This installer is for Arch Linux and Arch-based distributions only.")
print("Builds At github.com/Tuxlarper/Packed-QuickGrabber")
print("Under Creative Commons ShareAlike 4.0 International License.")

def ask_yes_no(prompt):
    """Ask for a yes/no response and repeat until it is valid."""
    answer = input(prompt).strip().lower()
    while answer not in ("yes", "y", "no", "n"):
        answer = input("Please enter yes or no: ").strip().lower()
    return answer


def run_with_sudo(command):
    """Run a command with sudo."""
    result = subprocess.run(["sudo", *command], check=False)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result


def offer_package(prompt, package):
    answer = ask_yes_no(prompt)
    if answer in ("yes", "y"):
        print("Continuing...")
        run_with_sudo(["pacman", "-S", "--needed", "--noconfirm", package])
    else:
        print("Skipped.")


def is_arch_based():
    try:
        os_release = platform.freedesktop_os_release()
    except (AttributeError, OSError):
        return False

    distro_id = os_release.get("ID", "").strip().lower()
    distro_like = os_release.get("ID_LIKE", "").lower().split()
    return distro_id == "arch" or "arch" in distro_like


can_continue = ask_yes_no("Do you know what this script will do? (yes/no): ")

if can_continue in ("no", "n"):
    print("Please read about the script before continuing:")
    print("https://github.com/Tuxlarper/Packed-QuickGrabber")
    print("Installation cancelled.")
else:
    print("This script will install the following applications:")
    print("Applications will be listed as you go.")

    proceed = ask_yes_no("Do you understand and still want to proceed? (yes/no): ")
    if proceed in ("no", "n"):
        print("Installation cancelled.")
    else:
        if not is_arch_based():
            print(
                "Unsupported or undetected distribution. This installer only supports "
                "Arch Linux and Arch-based distributions."
            )
            raise SystemExit(1)
        else:
            sudo_answer = ask_yes_no(
                "Allow this script to run its commands with sudo? (yes/no): "
            )
            if sudo_answer in ("no", "n"):
                print("Installation cancelled because sudo access was not granted.")
            elif shutil.which("sudo") is None:
                print("sudo is not installed. Installation cancelled.")
            else:
                sudo_check = subprocess.run(["sudo", "-v"], check=False)
                if sudo_check.returncode != 0:
                    print("sudo authentication failed. Installation cancelled.")
                else:
                    offer_package("Would You Like Firefox? (extra) (yes/no): ", "firefox")
                    answer = ask_yes_no("Would You Like A System Upgrade? (extra & core)(yes/no): ")
                    if answer in ("yes", "y"):
                        print("Continuing...")
                        run_with_sudo(["pacman", "-Syu", "--noconfirm"])
                    else:
                        print("Skipped.")

                    answer = ask_yes_no("Would You Like Clam Antivirus? (extra) (yes/no): ")
                    if answer in ("yes", "y"):
                        print("Continuing...")
                        run_with_sudo(["pacman", "-S", "--needed", "--noconfirm", "clamav"])
                        run_with_sudo(["freshclam"])
                    else:
                        print("Skipped.")

                    answer = ask_yes_no("Would You Like fastfetch & hyfetch? (extra) (yes/no): ")
                    if answer in ("yes", "y"):
                        print("Continuing...")
                        run_with_sudo(["pacman", "-S", "--needed", "--noconfirm", "fastfetch"])
                        run_with_sudo(["pacman", "-S", "--needed", "--noconfirm", "hyfetch"])
                    else:
                        print("Skipped.")

                    answer = ask_yes_no(
                        "Would you like to set up Flathub and Flatpak? (yes/no): "
                    )
                    if answer in ("yes", "y"):
                        print("Continuing...")
                        run_with_sudo(["pacman", "-S", "--needed", "--noconfirm", "flatpak"])
                        run_with_sudo(
                            [
                                "flatpak",
                                "remote-add",
                                "--if-not-exists",
                                "flathub",
                                "https://dl.flathub.org/repo/flathub.flatpakrepo",
                            ]
                        )
                    else:
                        print("Skipped.")

                    offer_package("Would You Like Discord? (extra)(yes/no): ", "discord")
                    offer_package("Would You Like Mullvad VPN? (Mullvad Repo)(yes/no): ", "mullvad-vpn")
                    offer_package("Would You Like Steam? (multilib repo required)(yes/no): ", "steam")
                    answer = ask_yes_no("Would You Like Spotify? (Flatpak Required)(yes/no): ")
                    if answer in ("yes", "y"):
                        print("Continuing...")
                        run_with_sudo(
                            [
                                "flatpak",
                                "install",
                                "--system",
                                "--noninteractive",
                                "flathub",
                                "com.spotify.Client",
                            ]
                        )
                    else:
                        print("Skipped.")
                    answer = ask_yes_no("Would You Like LibreWolf? (Flatpak Required)(yes/no): ")
                    if answer in ("yes", "y"):
                        print("Continuing...")
                        run_with_sudo(
                            [
                                "flatpak",
                                "install",
                                "--system",
                                "--noninteractive",
                                "flathub",
                                "io.gitlab.librewolf-community",
                            ]
                        )
                    else:
                        print("Skipped.")
                    offer_package("Would You Like Wine? (extra)(yes/no): ", "wine")
                    offer_package("Would You Like Lutris? (extra)(yes/no): ", "lutris")
                    offer_package("Would You Like OBS Studio? (extra)(yes/no): ", "obs-studio")
                    offer_package("Would You Like GIMP? (extra)(yes/no): ", "gimp")
                    offer_package("Would You Like Inkscape? (extra)(yes/no): ", "inkscape")
                    offer_package("Would You Like Blender? (extra)(yes/no): ", "blender")
                    offer_package("Would You Like Syncthing?) (extra)(yes/no): ", "syncthing")
                    offer_package("Would You Like KleoPatra? (no gpg suite, extra)(yes/no): ", "kleopatra")
                    offer_package("Would You Like Kdenlive? (extra)(yes/no): ", "kdenlive")
                    offer_package("Would You Like Krita? (extra)(yes/no): ", "krita")
                    offer_package("Would You Like Audacity? (extra)(yes/no): ", "audacity")

            answer = ask_yes_no("Would You Like Spicetify? (official script, no sudo)(yes/no): ")
            if answer in ("yes", "y"):
                if hasattr(os, "geteuid") and os.geteuid() == 0:
                    print("Spicetify must be installed as your normal user, not as root.")
                else:
                    print("Continuing...")
                    installer = subprocess.run(
                        [
                            "curl",
                            "-fsSL",
                            "https://raw.githubusercontent.com/spicetify/cli/main/install.sh",
                        ],
                        stdout=subprocess.PIPE,
                        check=False,
                    )
                    print("Downloading...")
                    if installer.returncode != 0:
                        print("Failed to download the Spicetify installer.")
                    else:
                        result = subprocess.run(
                            ["sh"],
                            input=installer.stdout,
                            check=False,
                        )
                        if result.returncode != 0:
                            print(
                                "Spicetify installer failed with exit code "
                                f"{result.returncode}."
                            )
            else:
                print("Skipped.")

#d293LCBmaXJzdCBwZXJzb24gaSBhaHZlIHNlZ
# W4gdG8gYWN0dWFsbHkgcmVhZCB0aGUgY29kZS4gYW
# 5kIHlvdSBkZWNvZGVkIHRoaXMhCi
# BAdHV4bGFycGVyIG9uIGdpdGh1Yg==
#lol
