import sys
import platform

def check_dependency(error, package_name):
    print(f"\nerror: {error}")
    print(f"package_name: {package_name}\n")


    print(f"which system.platform are you? >> {sys.platform} <<\n")
    if sys.platform == "linux":
        print(platform.freedesktop_os_release())
    elif sys.platform == "windows":
        print(platform.freedesktop_os_release())
    elif sys.platform == "darwin":
        print(platform.freedesktop_os_release())

    sys.exit(1)
        
        # print(f"sys props: \n\n{dir(sys)}")
        # for prop in dir(sys):
        #     print(prop)
        # print("")
        # print("")
        # print("")
        # print(f"platform props: \n\n{dir(platform)}")
        # for prop in dir(platform):
        #     print(prop)
        # print("")
        # print(f"{platform.system()}")
        # print("")
        # print(f"platform.system(): {platform.system()}")
        # print(f"platform.release(): {platform.release()}")

# print(check_dependancy())