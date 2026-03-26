import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Eye, EyeOff, Zap, TrendingUp, BarChart3 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const Login = () => {
  const navigate = useNavigate();
  const [showPassword, setShowPassword] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate("/setup");
  };

  return (
    <div className="min-h-screen flex bg-background bg-grid bg-radial-glow overflow-hidden relative">
      {/* Floating orbs */}
      <div className="absolute top-20 left-20 w-72 h-72 rounded-full bg-primary/5 blur-3xl animate-float" />
      <div className="absolute bottom-20 right-20 w-96 h-96 rounded-full bg-accent/5 blur-3xl animate-float" style={{ animationDelay: "2s" }} />
      <div className="absolute top-1/2 left-1/3 w-64 h-64 rounded-full bg-secondary/5 blur-3xl animate-float" style={{ animationDelay: "4s" }} />

      {/* Left - Branding */}
      <motion.div
        initial={{ opacity: 0, x: -40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.8 }}
        className="hidden lg:flex flex-1 flex-col justify-center items-center p-16 relative"
      >
        <div className="max-w-lg space-y-8">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-xl bg-primary/20 flex items-center justify-center glow-primary">
              <Zap className="w-6 h-6 text-primary" />
            </div>
            <h1 className="text-4xl font-display font-bold text-gradient-primary">Cheese popcorn</h1>
          </div>
          <p className="text-2xl font-display font-light text-foreground/80 leading-relaxed">
            AI-powered trend analysis & content generation for your brand
          </p>
          <div className="space-y-4 pt-4">
            {[
              { icon: TrendingUp, text: "Real-time trend monitoring" },
              { icon: BarChart3, text: "Competitor intelligence" },
              { icon: Zap, text: "Auto-generated content" },
            ].map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + i * 0.15 }}
                className="flex items-center gap-3 text-muted-foreground"
              >
                <div className="w-8 h-8 rounded-lg bg-muted flex items-center justify-center">
                  <item.icon className="w-4 h-4 text-primary" />
                </div>
                <span>{item.text}</span>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Right - Form */}
      <div className="flex-1 flex items-center justify-center p-6">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="w-full max-w-md"
        >
          <div className="glass-strong rounded-2xl p-8 space-y-6 glow-primary">
            <div className="text-center space-y-2">
              <div className="lg:hidden flex items-center justify-center gap-2 mb-4">
                <Zap className="w-6 h-6 text-primary" />
                <span className="text-2xl font-display font-bold text-gradient-primary">TrendPulse</span>
              </div>
              <h2 className="text-2xl font-display font-semibold text-foreground">
                {isSignUp ? "Create account" : "Welcome back"}
              </h2>
              <p className="text-muted-foreground text-sm">
                {isSignUp ? "Start analyzing trends today" : "Sign in to your dashboard"}
              </p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-4">
              {isSignUp && (
                <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "auto", opacity: 1 }}>
                  <label className="text-sm font-medium text-foreground/80 mb-1.5 block">Full Name</label>
                  <Input
                    placeholder="John Doe"
                    className="bg-muted/50 border-border/50 focus:border-primary/50 h-11"
                  />
                </motion.div>
              )}
              <div>
                <label className="text-sm font-medium text-foreground/80 mb-1.5 block">Email</label>
                <Input
                  type="email"
                  placeholder="you@company.com"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-muted/50 border-border/50 focus:border-primary/50 h-11"
                />
              </div>
              <div>
                <label className="text-sm font-medium text-foreground/80 mb-1.5 block">Password</label>
                <div className="relative">
                  <Input
                    type={showPassword ? "text" : "password"}
                    placeholder="••••••••"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="bg-muted/50 border-border/50 focus:border-primary/50 h-11 pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
                  >
                    {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  </button>
                </div>
              </div>

              <Button
                type="submit"
                className="w-full h-11 bg-primary text-primary-foreground font-semibold hover:bg-primary/90 transition-all glow-primary"
              >
                {isSignUp ? "Create Account" : "Sign In"}
              </Button>
            </form>

            <div className="relative">
              <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-border/50" /></div>
              <div className="relative flex justify-center text-xs"><span className="bg-card px-2 text-muted-foreground">or</span></div>
            </div>

            <Button
              variant="outline"
              className="w-full h-11 border-border/50 bg-muted/30 hover:bg-muted/50 text-foreground"
              onClick={handleSubmit}
            >
              Continue with Google
            </Button>

            <p className="text-center text-sm text-muted-foreground">
              {isSignUp ? "Already have an account?" : "Don't have an account?"}{" "}
              <button onClick={() => setIsSignUp(!isSignUp)} className="text-primary hover:underline font-medium">
                {isSignUp ? "Sign in" : "Sign up"}
              </button>
            </p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default Login;
