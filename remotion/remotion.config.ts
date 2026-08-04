import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
Config.setBrowserExecutable("/usr/bin/chromium");
Config.setChromiumOpenGlRenderer("swangle");
Config.setChromiumDisableWebSecurity(true);
