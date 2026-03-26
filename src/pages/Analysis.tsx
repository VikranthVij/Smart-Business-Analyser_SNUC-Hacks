import { motion } from "framer-motion";
import { TrendingUp, PieChart as PieIcon, BarChart3, ArrowRight } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { Button } from "@/components/ui/button";
import DashboardLayout from "@/components/DashboardLayout";
import { useEffect, useState } from "react";

const Analysis = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Get data from the 'state' passed by Setup.tsx
  const { companyName } = location.state || { 
    companyName: "Brand" 
  };

  const [analysisData, setAnalysisData] = useState<any>(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/analysis")
      .then(res => res.json())
      .then(data => setAnalysisData(data))
      .catch(err => console.error("Could not load backend analysis:", err));
  }, []);

  if (!analysisData) {
    return (
      <DashboardLayout>
        <div className="flex h-full items-center justify-center">
           <p className="text-muted-foreground animate-pulse">Loading intelligence insights...</p>
        </div>
      </DashboardLayout>
    );
  }

  // Convert distribution into chart-friendly data
  const dynamicPieData = Object.entries(analysisData.trend_distribution || {}).map(([key, val], i) => ({
    name: key,
    value: val,
    color: `hsl(${(i * 50) % 360}, 70%, 60%)`
  }));

  const dynamicBarData = Object.entries(analysisData.ad_signals || {}).slice(0, 5).map(([key, val]) => ({
    name: key.substring(0, 10),
    interest: val as number,
  }));

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-display font-bold">{companyName} Market Analysis</h1>
          <p className="text-muted-foreground">Found {dynamicPieData.length} active trends and 1 primary issue ({String(analysisData.top_issue)}) in your niche.</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pie Chart Card */}
          <div className="glass rounded-2xl p-6 border border-border/50">
            <h3 className="flex items-center gap-2 font-semibold mb-6">
              <PieIcon className="w-4 h-4 text-primary" /> Market Trend Distribution
            </h3>
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={dynamicPieData} innerRadius={60} outerRadius={90} paddingAngle={5} dataKey="value">
                    {dynamicPieData.map((entry, index) => (
                      <Cell key={index} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="grid grid-cols-2 gap-2 mt-4 max-h-32 overflow-y-auto">
              {dynamicPieData.map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-xs text-muted-foreground">
                  <div className="w-2 h-2 shrink-0 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="truncate">{item.name} ({String(item.value)})</span>
                </div>
              ))}
            </div>
          </div>

          {/* Bar Chart Card */}
          <div className="glass rounded-2xl p-6 border border-border/50">
            <h3 className="flex items-center gap-2 font-semibold mb-6">
              <BarChart3 className="w-4 h-4 text-secondary" /> Competitor Ad Focus Frequency
            </h3>
            <div className="h-[280px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={dynamicBarData}>
                  <XAxis dataKey="name" stroke="#888" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis hide />
                  <Tooltip cursor={{ fill: "rgba(255,255,255,0.05)" }} />
                  <Bar dataKey="interest" fill="hsl(187, 100%, 50%)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        {/* AI Insight Box */}
        <div className="p-6 rounded-2xl bg-primary/5 border border-primary/20">
          <h4 className="font-semibold flex items-center gap-2 mb-2 text-primary">
            <TrendingUp className="w-4 h-4" /> Strategic Opportunity & LangChain Insight
          </h4>
          <p className="text-sm text-foreground font-medium mb-2">
            Top Trend: <span className="font-bold text-primary">{String(analysisData.top_trend)}</span> | Focus Issue to Fix: <span className="font-bold text-destructive">{String(analysisData.top_issue)}</span>
          </p>
          <div className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">
            {String(analysisData.langchain_strategy || "")}
          </div>
        </div>

        <div className="flex justify-end pt-4">
          <Button
            onClick={() => navigate("/dashboard/generate", { state: { trends: Object.keys(analysisData.trend_distribution || {}) } })}
            className="h-11 px-8 bg-primary text-primary-foreground font-semibold gap-2"
          >
            Generate Content <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default Analysis;