import re

with open("src/features/marketing/domain/usecases/run_marketing_pipeline.py", "r") as f:
    code = f.read()

new_execute = """
    async def execute(self, config: PipelineConfig) -> PipelineResult:
        \"\"\"
        Runs the full pipeline in two resilient phases (Silver and Gold layers).
        \"\"\"

        # ------------------------------------------------------------------
        # PHASE 1: Bronze -> Silver (Clean, Translate, Normalize)
        # ------------------------------------------------------------------
        normalize_uc = CleanAndNormalizeUseCase(
            youtube_repo=self._youtube_repo,
            github_repo=self._github_repo,
            google_news_repo=self._google_news_repo,
            llm=self._llm,
            limit_per_source=config.limit_per_source,
            translate_non_english=config.translate_non_english,
        )
        items, stats = await normalize_uc.execute()

        # Save successful translations to Silver layer
        if items:
            await self._marketing_repo.save_many_normalized_items(items)
            
            # Mark raw sources as processed so we don't translate them again
            yt_ids = [item.raw_id for item in items if item.source == "youtube"]
            gh_ids = [int(item.raw_id) for item in items if item.source == "github"]
            gn_ids = [item.raw_id for item in items if item.source == "google_news"]

            if yt_ids:
                await self._youtube_repo.mark_as_processed(yt_ids)
            if gh_ids:
                await self._github_repo.mark_as_processed(gh_ids)
            if gn_ids:
                await self._google_news_repo.mark_as_processed(gn_ids)

        # ------------------------------------------------------------------
        # PHASE 2: Silver -> Gold (Filter, Cluster, Generate Campaigns)
        # ------------------------------------------------------------------
        # Fetch everything in the Silver layer that hasn't been used for marketing yet
        silver_items = await self._marketing_repo.find_unprocessed_normalized_items(limit=config.limit_per_source * 3)

        if not silver_items:
            return PipelineResult(
                campaigns=[],
                cleaning_stats=stats,
                clusters_found=0,
                items_processed=0,
                items_after_filter=0,
            )

        # Intent filter
        scored = IntentFilterUseCase().execute(silver_items, min_score=config.min_intent_score)

        if not scored:
            return PipelineResult(
                campaigns=[],
                cleaning_stats=stats,
                clusters_found=0,
                items_processed=len(silver_items),
                items_after_filter=0,
            )

        # Semantic clustering
        cluster_uc = ClusterContentUseCase(n_clusters=config.n_clusters)
        clusters = await cluster_uc.execute(scored)

        if clusters:
            try:
                clusters = await self._marketing_repo.save_many_clusters(clusters)
            except Exception as e:
                print(f"Bulk cluster save error: {e}")

        # LLM content generation
        gen_uc = GenerateMarketingContentUseCase(
            llm=self._llm,
            campaign_type=config.campaign_type,
        )

        generation_results = await asyncio.gather(
            *(gen_uc.execute(c) for c in clusters),
            return_exceptions=True,
        )

        campaigns: list[MarketingCampaign] = []
        for i, result in enumerate(generation_results):
            if isinstance(result, Exception):
                error_msg = str(result)
                print(f"Campaign generation error (cluster={clusters[i].topic_label}): {error_msg}")
                raise result
            else:
                campaigns.append(result)

        if campaigns:
            try:
                await self._marketing_repo.save_many_campaigns(campaigns)
            except Exception as e:
                print(f"Bulk campaign save error: {e}")
                raise e

        # Mark Silver items as fully processed
        silver_ids = [item.id for item in silver_items]
        if silver_ids:
            await self._marketing_repo.mark_normalized_as_processed(silver_ids)

        return PipelineResult(
            campaigns=campaigns,
            cleaning_stats=stats,
            clusters_found=len(clusters),
            items_processed=len(silver_items),
            items_after_filter=len(scored),
        )
"""

code = re.sub(r'    async def execute\(self, config: PipelineConfig\) -> PipelineResult:.*?(?=\Z)', new_execute, code, flags=re.DOTALL)

with open("src/features/marketing/domain/usecases/run_marketing_pipeline.py", "w") as f:
    f.write(code)

