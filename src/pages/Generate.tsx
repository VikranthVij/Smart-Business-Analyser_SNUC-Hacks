import { useState } from "react";
import { motion } from "framer-motion";
import { Wand2, Image, SlidersHorizontal, Tag, Send, RefreshCw, Download, Heart } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Slider } from "@/components/ui/slider";
import { Badge } from "@/components/ui/badge";
import DashboardLayout from "@/components/DashboardLayout";

const MOCK_IMAGES = [
  { id: 1, label: "Minimalist Product Shot", gradient: "from-primary/20 to-accent/20" },
  { id: 2, label: "Lifestyle Action", gradient: "from-secondary/20 to-primary/20" },
  { id: 3, label: "Urban Streetwear", gradient: "from-accent/20 to-secondary/20" },
  { id: 4, label: "Editorial Campaign", gradient: "from-primary/20 to-secondary/20" },
  { id: 5, label: "Social Story Format", gradient: "from-secondary/20 to-accent/20" },
  { id: 6, label: "Bold Typography", gradient: "from-accent/20 to-primary/20" },
];

const STYLE_KEYWORDS = [
  "Minimal", "Bold", "Vibrant", "Moody", "Clean", "Retro",
  "Futuristic", "Organic", "Professional", "Playful", "Elegant", "Raw",
];

const Generate = () => {
  const [prompt, setPrompt] = useState("");
  const [selectedStyles, setSelectedStyles] = useState<string[]>(["Minimal", "Bold"]);
  const [selectedImage, setSelectedImage] = useState<number | null>(null);
  const [settings, setSettings] = useState({
    creativity: [7],
    detail: [6],
    brandAlignment: [8],
    trendRelevance: [5],
  });
  const [generating, setGenerating] = useState(false);

  const toggleStyle = (s: string) => {
    setSelectedStyles((prev) =>
      prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s]
    );
  };

  const handleGenerate = () => {
    setGenerating(true);
    setTimeout(() => setGenerating(false), 2000);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-display font-bold text-foreground">Post Generator</h1>
          <p className="text-muted-foreground mt-1">AI-powered content creation based on your trends</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left: Controls */}
          <div className="lg:col-span-1 space-y-6">
            {/* Prompt */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="glass rounded-2xl p-6"
            >
              <div className="flex items-center gap-2 mb-4">
                <Wand2 className="w-5 h-5 text-primary" />
                <h3 className="font-display font-semibold text-foreground">Prompt</h3>
              </div>
              <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe the post you want to create... e.g. 'A trendy summer collection reveal with urban vibes'"
                rows={4}
                className="w-full bg-muted/30 border border-border/50 rounded-xl p-3 text-sm text-foreground placeholder:text-muted-foreground focus:border-primary/50 focus:outline-none resize-none"
              />
            </motion.div>

            {/* Style Keywords */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="glass rounded-2xl p-6"
            >
              <div className="flex items-center gap-2 mb-4">
                <Tag className="w-5 h-5 text-secondary" />
                <h3 className="font-display font-semibold text-foreground">Style Keywords</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {STYLE_KEYWORDS.map((s) => {
                  const active = selectedStyles.includes(s);
                  return (
                    <button
                      key={s}
                      onClick={() => toggleStyle(s)}
                      className={`px-3 py-1 rounded-lg text-xs font-medium transition-all ${
                        active
                          ? "bg-secondary/20 text-secondary border border-secondary/40"
                          : "bg-muted/40 text-muted-foreground border border-border/50 hover:border-secondary/30"
                      }`}
                    >
                      {s}
                    </button>
                  );
                })}
              </div>
            </motion.div>

            {/* Sliders */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="glass rounded-2xl p-6"
            >
              <div className="flex items-center gap-2 mb-4">
                <SlidersHorizontal className="w-5 h-5 text-accent" />
                <h3 className="font-display font-semibold text-foreground">Generation Settings</h3>
              </div>
              <div className="space-y-6">
                {[
                  { key: "creativity" as const, label: "Creativity", left: "Conservative", right: "Wild" },
                  { key: "detail" as const, label: "Detail Level", left: "Simple", right: "Rich" },
                  { key: "brandAlignment" as const, label: "Brand Alignment", left: "Flexible", right: "Strict" },
                  { key: "trendRelevance" as const, label: "Trend Relevance", left: "Evergreen", right: "Trending" },
                ].map((slider) => (
                  <div key={slider.key} className="space-y-2">
                    <div className="flex justify-between items-center">
                      <label className="text-xs font-medium text-foreground">{slider.label}</label>
                      <span className="text-xs font-mono text-primary">{settings[slider.key][0]}</span>
                    </div>
                    <Slider
                      value={settings[slider.key]}
                      onValueChange={(val) => setSettings((prev) => ({ ...prev, [slider.key]: val }))}
                      max={10}
                      min={0}
                      step={1}
                      className="[&_[role=slider]]:bg-primary [&_[role=slider]]:border-primary"
                    />
                    <div className="flex justify-between text-[10px] text-muted-foreground">
                      <span>{slider.left}</span>
                      <span>{slider.right}</span>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            <Button
              onClick={handleGenerate}
              disabled={generating}
              className="w-full h-12 bg-primary text-primary-foreground font-semibold gap-2 hover:bg-primary/90 glow-primary"
            >
              {generating ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Send className="w-4 h-4" />
                  Generate Posts
                </>
              )}
            </Button>
          </div>

          {/* Right: Image Options */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="glass rounded-2xl p-6"
            >
              <div className="flex items-center gap-2 mb-6">
                <Image className="w-5 h-5 text-primary" />
                <h3 className="font-display font-semibold text-foreground">Generated Options</h3>
                <Badge variant="secondary" className="bg-primary/10 text-primary border-primary/20 ml-auto">
                  {MOCK_IMAGES.length} variants
                </Badge>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {MOCK_IMAGES.map((img, i) => (
                  <motion.button
                    key={img.id}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: 0.3 + i * 0.08 }}
                    onClick={() => setSelectedImage(img.id)}
                    className={`group relative aspect-square rounded-xl overflow-hidden border-2 transition-all ${
                      selectedImage === img.id
                        ? "border-primary glow-primary"
                        : "border-border/30 hover:border-primary/40"
                    }`}
                  >
                    <div className={`absolute inset-0 bg-gradient-to-br ${img.gradient}`} />
                    <div className="absolute inset-0 bg-grid opacity-20" />

                    {/* Simulated content */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-4">
                      <div className="w-16 h-16 rounded-2xl bg-foreground/5 backdrop-blur-sm border border-foreground/10 flex items-center justify-center mb-3">
                        <Image className="w-8 h-8 text-foreground/30" />
                      </div>
                      <span className="text-xs font-medium text-foreground/60 text-center">{img.label}</span>
                    </div>

                    {/* Hover overlay */}
                    <div className="absolute inset-0 bg-background/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-2">
                      <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                        <Heart className="w-4 h-4 text-primary" />
                      </div>
                      <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
                        <Download className="w-4 h-4 text-primary" />
                      </div>
                    </div>

                    {selectedImage === img.id && (
                      <div className="absolute top-2 right-2 w-6 h-6 rounded-full bg-primary flex items-center justify-center">
                        <svg className="w-3 h-3 text-primary-foreground" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                    )}
                  </motion.button>
                ))}
              </div>

              {selectedImage && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="mt-6 p-4 rounded-xl bg-muted/30 border border-border/30"
                >
                  <h4 className="text-sm font-semibold text-foreground mb-2">Post Preview</h4>
                  <p className="text-sm text-muted-foreground leading-relaxed">
                    🔥 Redefining urban style this season. Our latest drop combines <span className="text-primary">sustainable materials</span> with 
                    street-ready aesthetics. Bold silhouettes, muted tones, and a commitment to the future. 
                    <span className="text-secondary"> #FashionForward #StreetStyle #Sustainable</span>
                  </p>
                  <div className="flex gap-2 mt-3">
                    <Button size="sm" className="bg-primary text-primary-foreground hover:bg-primary/90 gap-1">
                      <Download className="w-3 h-3" /> Export
                    </Button>
                    <Button size="sm" variant="outline" className="border-border/50 gap-1">
                      <RefreshCw className="w-3 h-3" /> Regenerate
                    </Button>
                  </div>
                </motion.div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Generate;
