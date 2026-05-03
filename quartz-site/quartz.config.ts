import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

const config: QuartzConfig = {
  configuration: {
    pageTitle: "🥥 椰子要破壳",
    pageTitleSuffix: " · 八字入门",
    enableSPA: true,
    enablePopovers: true,
    analytics: null,
    locale: "zh-CN",
    baseUrl: "sunyanyanyan.github.io/mingli-xue",
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Noto Serif SC",
        body: "Noto Sans SC",
        code: "JetBrains Mono",
      },
      colors: {
        lightMode: {
          light: "#FFF8E1",
          lightgray: "#E8D5B7",
          gray: "#A0937D",
          darkgray: "#5D4E37",
          dark: "#3E2C1C",
          secondary: "#558B2F",
          tertiary: "#FF8F00",
          highlight: "rgba(121, 85, 72, 0.12)",
          textHighlight: "#FF8F0066",
        },
        darkMode: {
          light: "#1A1410",
          lightgray: "#2E2418",
          gray: "#6B5B4A",
          darkgray: "#D4C5B2",
          dark: "#F5EDE0",
          secondary: "#7CB342",
          tertiary: "#FFB300",
          highlight: "rgba(255, 143, 0, 0.12)",
          textHighlight: "#FFB30066",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
    ],
  },
}

export default config
