import cProfile
import pstats


def load_in_batches(data: list, size: int):
    for _ in range(0, len(data), size):
        batch = data[_ : size + _]
        yield batch


def profiler(report_name="profiler_report.prof", limit=10):
    def report(func):
        def wrapper(self, *args, **kwargs):
            with cProfile.Profile() as profile:
                result = func(self, *args, **kwargs)
            # reminder: save profiling results to a file
            profile.dump_stats(report_name)
            # reminder: print profiling statistics to console
            stats = pstats.Stats(report_name)
            stats.strip_dirs()
            stats.sort_stats("cumulative")
            stats.print_stats(limit)
            return result

        return wrapper

    return report
