import multiprocessing


class MyProcess(multiprocessing.Process):
    def run(self) -> None:
        print("Procesul")