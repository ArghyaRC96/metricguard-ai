# Total Orders Metric Semantics

author: Priya Nair
team: Data Analytics
date: 2026-01-13
related_metric: total_orders

Operations and Finance intentionally use different order-counting concepts.

Operations needs visibility into operational workload and therefore counts all
placed orders except cancelled orders.

The enterprise Total Orders KPI introduced in December 2025 counts successfully
paid orders.

The two measures should not be directly compared without understanding their
business context.

This difference is intentional and should not be classified as a broken data
pipeline.
