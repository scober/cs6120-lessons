#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct SkeletonPass : public PassInfoMixin<SkeletonPass> {
  PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
    for (auto &F : M) {
      LLVMContext& Ctx = F.getContext();


      std::vector<Type*> paramTypes = {Type::getInt32Ty(Ctx)};
      Type *retType = Type::getVoidTy(Ctx);
      FunctionType *logFuncType = FunctionType::get(retType, paramTypes, false);
      FunctionCallee logFunc =
          F.getParent()->getOrInsertFunction("logint", logFuncType);

      for (auto &B : F) {
        for (auto &I : B) {
          if (auto *BO = dyn_cast<BinaryOperator>(&I)) {
            errs() << "op:\n";
            BO->print(errs());
            errs() << '\n';

            IRBuilder<> builder(BO);
            builder.SetInsertPoint(&B, ++builder.GetInsertPoint());

            Value* args[] = {BO};
            builder.CreateCall(logFunc, args);
            Value* lhs = BO->getOperand(0);
            Value* rhs = BO->getOperand(1);

            errs() << "lhs:\n    ";
            lhs->print(errs());
            errs() << '\n';
            errs() << "rhs:\n    ";
            rhs->print(errs());
          }
        }
      }
    }
    errs() << '\n';
    errs() << '\n';
    return PreservedAnalyses::none();
  };
};

}

extern "C" LLVM_ATTRIBUTE_WEAK ::llvm::PassPluginLibraryInfo
llvmGetPassPluginInfo() {
    return {
        .APIVersion = LLVM_PLUGIN_API_VERSION,
        .PluginName = "Skeleton pass",
        .PluginVersion = "v0.1",
        .RegisterPassBuilderCallbacks = [](PassBuilder &PB) {
            PB.registerPipelineStartEPCallback(
                [](ModulePassManager &MPM, OptimizationLevel Level) {
                    MPM.addPass(SkeletonPass());
                });
        }
    };
}
