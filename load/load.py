import sample_creator
import batch_creator
from multiprocessing import Event


class DataLoader:

    def __init__(self, data_store, batch_size=10):
        """
          Start the batchCreator and sampleCreator.
          Read the memory config file, and create the right number
          of processes.
        """
        self.ds = data_store
        self.ds.batch_size = batch_size
        # Event to stop batch creator and sample creator
        self.event = Event()

        # Start separate processes for sample_creator(s)
        sc = sample_creator.SampleCreator(self.ds, self.event)
        sc.start()

        # Start batch_creator(s)
        bc = batch_creator.BatchCreator(self.ds, self.event)
        bc.start()

        # Wait for sub-processes to terminate
        sc.join()
        bc.join()

    def get_next_batch(self):
        """
         Get the next batch from the queue
        """
        # Access batches from data_store.batches and return the batch
        # delete the used batch

        return self.ds.batches.get()

    def stop_batch_creation(self):
        self.event.set()



