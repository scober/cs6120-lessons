#include <stdlib.h>

#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Instruction.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

struct SkeletonPass : public PassInfoMixin<SkeletonPass> {
  PreservedAnalyses run(Module &M, ModuleAnalysisManager &AM) {
    for (auto &F : M) {
      LLVMContext& Ctx = F.getContext();

      //std::vector<Type*> paramTypes = {Type::getInt32Ty(Ctx)};
      //Type *retType = Type::getVoidTy(Ctx);
      //FunctionType *logFuncType = FunctionType::get(retType, paramTypes, false);
      //FunctionCallee logFunc =
      //    F.getParent()->getOrInsertFunction("logint", logFuncType);
      
      std::vector<Type*> paramTypes = {};
      Type *retType = Type::getVoidTy(Ctx);
      FunctionType *logFuncType = FunctionType::get(retType, paramTypes, false);
      FunctionCallee allocFunc =
          F.getParent()->getOrInsertFunction("alloc_one", logFuncType);

      //std::vector<Type*> paramTypes = {Type::getInt32Ty(Ctx)};
      //Type *retType = Type::getVoidTy(Ctx);
      //FunctionType *logFuncType = FunctionType::get(retType, paramTypes, false);
      //FunctionCallee allocFunc =
      //    F.getParent()->getOrInsertFunction("alloc_some", logFuncType);

      //auto& entryBlock = F.getEntryBlock();
      //auto& entryBlock = *F.begin();
      //auto& firstInstruction = *entryBlock.begin();
      //IRBuilder<> builder(&firstInstruction);

      for (auto &B : F) {
        for (auto &I : B) {
          if (auto* op = dyn_cast<BinaryOperator>(&I)) {
            if (op->getOpcode() == Instruction::Add && (rand() % 10) == 0) {
              IRBuilder<> builder(op);
              builder.CreateCall(allocFunc);
            }
          }
        }
      }
    }
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
