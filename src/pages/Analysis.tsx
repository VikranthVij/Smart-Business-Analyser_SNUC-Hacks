import { motion } from "framer-motion";
import { TrendingUp, PieChart as PieIcon, BarChart3, ArrowRight } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";
import { Button } from "@/components/ui/button";
import DashboardLayout from "@/components/DashboardLayout";

const Analysis = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Get data from the 'state' passed by Setup.tsx
  const { trends, companyName } = location.state || { 
    trends: ["No data fetched"], 
    companyName: "Brand" 
  };

  // Convert string trends into chart-friendly data
  const dynamicPieData = trends.map((trend: string, i: number) => ({
    name: trend,
    value: Math.floor(Math.random() * 25) + 15, // Mock percentage
    color: `hsl(${(i * 50) % 360}, 70%, 60%)`
  }));

  const dynamicBarData = trends.slice(0, 5).map((trend: string) => ({
    name: trend.substring(0, 10),
    interest: Math.floor(Math.random() * 100),
  }));

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="text-3xl font-display font-bold">{companyName} Market Analysis</h1>
          <p className="text-muted-foreground">Found {trends.length} high-growth trends in your niche.</p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Pie Chart Card */}
          <div className="glass rounded-2xl p-6 border border-border/50">
            <h3 className="flex items-center gap-2 font-semibold mb-6">
              <PieIcon className="w-4 h-4 text-primary" /> Topic Distribution
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
            <div className="grid grid-cols-2 gap-2 mt-4">
              {dynamicPieData.map((item, i) => (
                <div key={i} className="flex items-center gap-2 text-xs text-muted-foreground">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: item.color }} />
                  <span className="truncate">{item.name}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Bar Chart Card */}
          <div className="glass rounded-2xl p-6 border border-border/50">
            <h3 className="flex items-center gap-2 font-semibold mb-6">
              <BarChart3 className="w-4 h-4 text-secondary" /> Interest Score
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
            <TrendingUp className="w-4 h-4" /> Strategic Opportunity
          </h4>
          <p className="text-sm text-muted-foreground leading-relaxed">
            Based on our live scan, <span className="text-foreground font-bold">{trends[0]}</span> is your biggest growth lever. 
            We recommend prioritizing this trend in your upcoming marketing materials.
          </p>
        </div>

        <div className="flex justify-end pt-4">
          <Button
            onClick={() => navigate("/dashboard/generate", { state: { trends } })}
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