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

      std::vector<Type*> paramTypes = {};
      Type *retType = Type::getVoidTy(Ctx);
      FunctionType *logFuncType = FunctionType::get(retType, paramTypes, false);
      FunctionCallee allocFunc =
          F.getParent()->getOrInsertFunction("alloc_one", logFuncType);

      auto& entryBlock = F.getEntryBlock();
      //BasicBlock* block = &entryBlock;
      //// I believe an empty block is ill-formed according to the LLVM spec, but
      ////   I am running across them
      //while (block->begin() == block->end()) {
      //  block = block->getUniqueSuccessor();
      //}
      //IRBuilder<> builder(&*block->getFirstInsertionPt());

      IRBuilder<> builder(&entryBlock, entryBlock.getFirstInsertionPt());
      builder.CreateCall(allocFunc);
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
