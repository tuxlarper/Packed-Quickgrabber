import subprocess
import shutil
import platform
import os
import shlex
# Under The Creative Commons ShareAlike 4.0 International License.
#Feel Free To ReDistrubute, Modify, And Share This Code. Just Give Credit To Me! @tuxlarper
#Orginal Github Repo: github.com/Tuxlarper/Packed-QuickGrabber
print("QuickGrabber Debian APT Installer")
print("Developed By Tuxlarper And Fully Open Source. Made With Love")
print("This installer is for Debian and Debian-based distributions only.")
print("Builds At github.com/Tuxlarper/Packed-QuickGrabber")
print("Under Creative Commons ShareAlike 4.0 International License.")

def ask_yes_no(prompt):
    """Ask for a yes/no response and repeat until it is valid."""
    answer = input(prompt).strip().lower()
    while answer not in ("yes", "y", "no", "n"):
        answer = input("Please enter yes or no: ").strip().lower()
    return answer


def run_with_sudo(command):
    """Run a command with the current user's approved privilege level."""
    prefix = [] if hasattr(os, "geteuid") and os.geteuid() == 0 else ["sudo"]
    result = subprocess.run([*prefix, *command], check=False)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}: {' '.join(command)}")
    return result


def package_is_available(package):
    """Return whether apt has a candidate for this package."""
    result = subprocess.run(
        ["apt-cache", "policy", package],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "LC_ALL": "C"},
    )
    if result.returncode != 0:
        return False
    for line in result.stdout.splitlines():
        if line.startswith("Candidate:"):
            return line.split(":", 1)[1].strip() not in ("", "(none)")
    return False


def offer_package(prompt, package):
    answer = ask_yes_no(prompt)
    if answer in ("yes", "y"):
        if not package_is_available(package):
            print(
                f"Package '{package}' is unavailable from the configured apt "
                "repositories. Enable the required repository and try again."
            )
            return
        print("Continuing...")
        run_with_sudo(["apt-get", "install", "-y", package])
    else:
        print("Skipped.")


def offer_flatpak(prompt, app_id):
    answer = ask_yes_no(prompt)
    if answer in ("yes", "y"):
        flatpak = shutil.which("flatpak")
        if flatpak is None:
            print("Flatpak is not installed. Set up Flatpak first; skipping.")
            return
        remotes = subprocess.run(
            [flatpak, "remotes", "--system", "--columns=name"],
            check=False,
            capture_output=True,
            text=True,
        )
        if remotes.returncode != 0:
            print("Could not check system Flatpak remotes. Skipping.")
            return
        if "flathub" not in {
            line.strip().lower() for line in remotes.stdout.splitlines()
        }:
            print(
                "The system Flathub remote is not configured. "
                "Set up Flatpak first; skipping."
            )
            return
        print("Continuing...")
        run_with_sudo(
            [
                "flatpak",
                "install",
                "--system",
                "--noninteractive",
                "flathub",
                app_id,
            ]
        )
    else:
        print("Skipped.")


def is_debian_based():
    try:
        os_release = platform.freedesktop_os_release()
    except AttributeError:
        try:
            os_release = {}
            with open("/etc/os-release", encoding="utf-8") as release_file:
                for line in release_file:
                    key, separator, raw_value = line.partition("=")
                    if not separator or key not in ("ID", "ID_LIKE"):
                        continue
                    try:
                        value = shlex.split(raw_value.strip())
                    except ValueError:
                        return False
                    if len(value) > 1:
                        return False
                    os_release[key] = value[0] if value else ""
        except OSError:
            return False
    except OSError:
        return False

    distro_id = os_release.get("ID", "").strip().lower()
    distro_like = os_release.get("ID_LIKE", "").lower().split()
    return distro_id in ("debian", "ubuntu") or "debian" in distro_like


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
        if not is_debian_based():
            print(
                "Unsupported or undetected distribution. This installer only supports "
                "Debian and Debian-based distributions."
            )
            raise SystemExit(1)
        elif shutil.which("apt-get") is None:
            print("apt-get is not installed. Installation cancelled.")
        elif not (hasattr(os, "geteuid") and os.geteuid() == 0) and shutil.which("sudo") is None:
            print("sudo is not installed. Installation cancelled.")
        else:
            privileged_answer = ask_yes_no(
                "Allow this script to run privileged package commands? (yes/no): "
            )
            if privileged_answer in ("no", "n"):
                print("Installation cancelled because privileged access was not granted.")
            else:
                running_as_root = hasattr(os, "geteuid") and os.geteuid() == 0
                sudo_check = (
                    subprocess.run(["sudo", "-v"], check=False)
                    if not running_as_root
                    else None
                )
                if sudo_check is not None and sudo_check.returncode != 0:
                    print("sudo authentication failed. Installation cancelled.")
                else:
                    update = run_with_sudo(["apt-get", "update"])
                    if update.returncode != 0:
                        print("Package list update failed. Installation cancelled.")
                    else:
                        offer_package(
                            "Would You Like Firefox ESR? (extra) (yes/no): ",
                            "firefox-esr",
                        )
                        answer = ask_yes_no(
                            "Would You Like A System Upgrade? (extra & core)(yes/no): "
                        )
                        if answer in ("yes", "y"):
                            print("Continuing...")
                            run_with_sudo(["apt-get", "upgrade", "-y"])
                        else:
                            print("Skipped.")

                        answer = ask_yes_no("Would You Like Clam Antivirus? (extra) (yes/no): ")
                        if answer in ("yes", "y"):
                            clamav_packages = ("clamav", "clamav-freshclam")
                            missing_clamav_packages = [
                                package
                                for package in clamav_packages
                                if not package_is_available(package)
                            ]
                            if not missing_clamav_packages:
                                print("Continuing...")
                                clamav_install = run_with_sudo(
                                    [
                                        "apt-get",
                                        "install",
                                        "-y",
                                        *clamav_packages,
                                    ]
                                )
                                if clamav_install.returncode == 0:
                                    run_with_sudo(["freshclam"])
                            else:
                                print(
                                    "Unavailable from the configured apt repositories: "
                                    + ", ".join(missing_clamav_packages)
                                )
                        else:
                            print("Skipped.")

                        answer = ask_yes_no(
                            "Would You Like fastfetch & hyfetch? (extra) (yes/no): "
                        )
                        if answer in ("yes", "y"):
                            available = [
                                package
                                for package in ("fastfetch", "hyfetch")
                                if package_is_available(package)
                            ]
                            unavailable = sorted({"fastfetch", "hyfetch"} - set(available))
                            if available:
                                print("Continuing...")
                                run_with_sudo(["apt-get", "install", "-y", *available])
                            if unavailable:
                                print(
                                    "Unavailable from the configured apt repositories: "
                                    + ", ".join(unavailable)
                                )
                        else:
                            print("Skipped.")

                        answer = ask_yes_no(
                            "Would you like to set up Flathub and Flatpak? (yes/no): "
                        )
                        if answer in ("yes", "y"):
                            print("Continuing...")
                            flatpak_install = run_with_sudo(
                                ["apt-get", "install", "-y", "flatpak"]
                            )
                            if flatpak_install.returncode == 0:
                                run_with_sudo(
                                    [
                                        "flatpak",
                                        "remote-add",
                                        "--if-not-exists",
                                        "--system",
                                        "flathub",
                                        "https://dl.flathub.org/repo/flathub.flatpakrepo",
                                    ]
                                )
                        else:
                            print("Skipped.")

                        offer_flatpak(
                            "Would You Like Discord? (Flatpak Required)(yes/no): ",
                            "com.discordapp.Discord",
                        )
                        offer_package(
                            "Would You Like Mullvad VPN? (Mullvad apt repo required)(yes/no): ",
                            "mullvad-vpn",
                        )
                        offer_package(
                            "Would You Like Steam? (contrib/non-free or multiverse repo required)(yes/no): ",
                            "steam",
                        )
                        offer_flatpak(
                            "Would You Like Spotify? (Flatpak Required)(yes/no): ",
                            "com.spotify.Client",
                        )
                        offer_flatpak(
                            "Would You Like LibreWolf? (Flatpak Required)(yes/no): ",
                            "io.gitlab.librewolf-community",
                        )
                        offer_package("Would You Like Wine? (extra)(yes/no): ", "wine")
                        offer_package("Would You Like Lutris? (extra)(yes/no): ", "lutris")
                        offer_package("Would You Like OBS Studio? (extra)(yes/no): ", "obs-studio")
                        offer_package("Would You Like GIMP? (extra)(yes/no): ", "gimp")
                        offer_package("Would You Like Inkscape? (extra)(yes/no): ", "inkscape")
                        offer_package("Would You Like Blender? (extra)(yes/no): ", "blender")
                        offer_package("Would You Like Syncthing? (extra)(yes/no): ", "syncthing")
                        offer_package("Would You Like Kleopatra? (extra)(yes/no): ", "kleopatra")
                        offer_package("Would You Like Kdenlive? (extra)(yes/no): ", "kdenlive")
                        offer_package("Would You Like Krita? (extra)(yes/no): ", "krita")
                        offer_package("Would You Like Audacity? (extra)(yes/no): ", "audacity")

