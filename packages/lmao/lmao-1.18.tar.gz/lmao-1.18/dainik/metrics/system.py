import time
import psutil
import threading
from queue import Queue

from dainik.proto.lmao_pb2 import *

import GPUtil
HAS_GPU = len(GPUtil.getGPUs())

def get_metrics_dict():
  cpu_usage = psutil.cpu_percent(percpu=True)
  # total_memory = psutil.virtual_memory().total
  data = {
    "cpu_usage": sum(cpu_usage) / len(cpu_usage),
    "memory_available": psutil.virtual_memory().available // (1024 ** 2),
    "memory_usage": psutil.virtual_memory().used // (1024 ** 2),
    "memory_percentage": psutil.virtual_memory().percent,
    "disk_utilisation": psutil.disk_usage('/').percent
  }
  if HAS_GPU:
    data.update({
      "gpu_usage": GPUtil.getGPUs()[0].load,
      "gpu_memory_available": GPUtil.getGPUs()[0].memoryFree // (1024 ** 2),
      "gpu_memory_usage": GPUtil.getGPUs()[0].memoryUsed // (1024 ** 2)
    })
  return data


class SystemMetricsLogger:
  def __init__(self, dk: 'dainik.Dainik', log_every: int = 1) -> None:
    self.dk = dk
    self.log_every = log_every

    # create a rate limiting mechanism
    self._queue = Queue()
    self._bar = threading.Barrier(2)
    def _rate_limiter(s = log_every):
      while True:
        self._bar.wait()
        time.sleep(s)
    self.rl = threading.Thread(target=_rate_limiter, daemon=True)
    self.rl.start()

    # create a thread to create metrics
    self.metrics_logger = threading.Thread(target=self._create_metrics_dict, daemon=True)
    self.metrics_logger.start()

    # So this function returns the latest cpu usage thast it has gathered from the previous call
    # and so we need to do an init fire to avoid getting 0.0
    psutil.cpu_percent(percpu=True)

  def _create_metrics_dict(self):
    while True:
      if self.dk.completed:
        break
      data = get_metrics_dict()
      self._queue.put(data)
      run_comp = self.log()
      if run_comp:
        break
      time.sleep(self.log_every)

  def log(self) -> bool:
    if self.dk.completed:
      return True
    self._bar.wait()
    items = []
    while not self._queue.empty():
      items.append(self._queue.get())
    for x in items:
      self.dk.log(x, log_type=RunLog.LogType.SYSTEM)
    return False

  def __del__(self):
    self._bar.wait()
    self._bar.wait()
    self.rl.join()
    self.metrics_logger.join()


if __name__ == "__main__":
  import json
  print(json.dumps(get_metrics_dict(), indent=2))
