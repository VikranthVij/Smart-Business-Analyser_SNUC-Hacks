import { ReactNode } from "react";
import { NavLink } from "react-router-dom";
import { BarChart3, Wand2, Settings, Zap, LogOut } from "lucide-react";
import { useNavigate, useLocation } from "react-router-dom";

const navItems = [
  { to: "/dashboard/analysis", icon: BarChart3, label: "Analysis" },
  { to: "/dashboard/generate", icon: Wand2, label: "Generate" },
];

const DashboardLayout = ({ children }: { children: ReactNode }) => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <div className="min-h-screen bg-background bg-grid flex">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border/50 bg-card/40 backdrop-blur-xl flex flex-col">
        <div className="p-5 border-b border-border/30">
          <button onClick={() => navigate("/")} className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center">
              <Zap className="w-4 h-4 text-primary" />
            </div>
            <span className="text-lg font-display font-bold text-gradient-primary">TrendPulse</span>
          </button>
        </div>

        <nav className="flex-1 p-3 space-y-1">
          {navItems.map((item) => {
            const active = location.pathname === item.to;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-all ${
                  active
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted/30"
                }`}
              >
                <item.icon className="w-4 h-4" />
                {item.label}
              </NavLink>
            );
          })}
        </nav>

        <div className="p-3 border-t border-border/30 space-y-1">
          <button className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-muted-foreground hover:text-foreground hover:bg-muted/30 w-full transition-all">
            <Settings className="w-4 h-4" />
            Settings
          </button>
          <button
            onClick={() => navigate("/")}
            className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-muted-foreground hover:text-destructive hover:bg-destructive/5 w-full transition-all"
          >
            <LogOut className="w-4 h-4" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="flex-1 p-8 overflow-auto bg-radial-glow">
        {children}
      </main>
    </div>
  );
};

export default DashboardLayout;
