from prometheus_client import Counter, Histogram

class MetricsService:
    def __init__(self):
        self.cache_hits = Counter(
            'cache_hits_total',
            'Total number of cache hits',
            ['cache_type']
        )
        
        self.cache_misses = Counter(
            'cache_misses_total',
            'Total number of cache misses',
            ['cache_type']
        )
        
        self.error_counter = Counter(
            'errors_total',
            'Total number of errors',
            ['error_type', 'chain_id']
        )

metrics_service = MetricsService()
