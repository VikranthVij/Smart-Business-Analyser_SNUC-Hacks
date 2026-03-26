import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Building2, Tag, Users, Plus, X, ArrowRight, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";

const KEYWORD_SUGGESTIONS = [
  "Clothing", "Fashion", "Streetwear", "Luxury", "Sustainable", "Activewear",
  "Vintage", "Minimalist", "Boho", "Athleisure", "Denim", "Couture"
];

const Setup = () => {
  const navigate = useNavigate();
  const [company, setCompany] = useState("");
  const [selectedKeywords, setSelectedKeywords] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const toggleKeyword = (kw: string) => {
    setSelectedKeywords((prev) =>
      prev.includes(kw) ? prev.filter((k) => k !== kw) : [...prev, kw]
    );
  };

  const handleRunAnalysis = async () => {
    setIsLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/trends", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ keywords: selectedKeywords }),
      });

      if (!response.ok) throw new Error("Backend connection failed");

      const data = await response.json();

      // Pass backend results to the Analysis page
      navigate("/dashboard/analysis", { 
        state: { 
          trends: data.trends,
          companyName: company 
        } 
      });
    } catch (error) {
      console.error("Error:", error);
      alert("Make sure your Python server (aura.py) is running on port 8000!");
    } finally {
      setIsLoading(false);
    }
  };

  const canProceed = company.length > 0 && selectedKeywords.length > 0;

  return (
    <div className="min-h-screen p-8 bg-background flex items-center justify-center">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="max-w-2xl w-full space-y-8">
        <section className="space-y-4">
          <h2 className="text-2xl font-display font-bold flex items-center gap-2">
            <Building2 className="w-6 h-6 text-primary" /> Brand Identity
          </h2>
          <Input 
            placeholder="Enter your company name..." 
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="h-12 bg-muted/30 border-border/50"
          />
        </section>

        <section className="space-y-4">
          <h2 className="text-2xl font-display font-bold flex items-center gap-2">
            <Tag className="w-6 h-6 text-secondary" /> Focus Keywords
          </h2>
          <div className="flex flex-wrap gap-2">
            {KEYWORD_SUGGESTIONS.map((kw) => (
              <Badge
                key={kw}
                variant={selectedKeywords.includes(kw) ? "default" : "outline"}
                className={`cursor-pointer py-2 px-4 text-sm transition-all ${
                  selectedKeywords.includes(kw) ? "bg-primary glow-primary" : "hover:bg-muted"
                }`}
                onClick={() => toggleKeyword(kw)}
              >
                {kw}
              </Badge>
            ))}
          </div>
        </section>

        <div className="flex justify-end pt-6">
          <Button
            onClick={handleRunAnalysis}
            disabled={!canProceed || isLoading}
            className="h-12 px-8 bg-primary text-primary-foreground font-semibold text-lg gap-2"
          >
            {isLoading ? (
              <><Loader2 className="w-5 h-5 animate-spin" /> Fetching Trends...</>
            ) : (
              <>Run Analysis <ArrowRight className="w-5 h-5" /></>
            )}
          </Button>
        </div>
      </motion.div>
    </div>
  );
};

export default Setup;