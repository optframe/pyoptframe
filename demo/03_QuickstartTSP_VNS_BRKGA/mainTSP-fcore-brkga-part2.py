
def mycallback_constructive_rsk(problemCtx: ProblemContextTSP) -> RSKSolutionTSP:
    sol = RKSolutionTSP()
    for i in range(problemCtx.n):
        key = random.choice([0, 100000]) / 100000.0
        sol.rkeys.append(key)
    sol.n = problemCtx.n
    return sol



class MyRandomKeysInitPop : public InitialEPopulation<std::pair<std::vector<double>, Evaluation<int>>>
{
   using RSK = std::vector<double>;

private:
   int sz;
   sref<RandGen> rg;

public:
   MyRandomKeysInitPop(int size, sref<RandGen> _rg = new RandGen)
     : sz{ size }
     , rg{ _rg }
   {
   }

   // copy constructor
   MyRandomKeysInitPop(const MyRandomKeysInitPop& self)
     : sz{ self.sz }
     , rg{ self.rg }
   {
   }

   virtual bool canEvaluate() const override
   {
      return false; // cannot evaluate
   }

   VEPopulation<std::pair<RSK, Evaluation<int>>> generateEPopulation(unsigned populationSize, double timelimit) override
   {
      VEPopulation<std::pair<RSK, Evaluation<int>>> pop;

      for (unsigned i = 0; i < populationSize; i++) {
         vector<double> vd(sz);
         for (int j = 0; j < sz; j++)
            vd[j] = (rg->rand() % 100000) / 100000.0;
         std::pair<RSK, Evaluation<int>> ind{ vd, Evaluation<int>{} };
         pop.push_back(ind);
      }

      return pop;
   }
};