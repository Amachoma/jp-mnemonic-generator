from mnemonic.generator import MnemonicGenerator, RunMode

if __name__ == "__main__":
    generator = MnemonicGenerator(dataset_path="./stream_parser/mnemonic_dataset.txt",
                                  output_path="./out/mnemonics.txt")
    generator.run(RunMode.INTERACTIVE)
