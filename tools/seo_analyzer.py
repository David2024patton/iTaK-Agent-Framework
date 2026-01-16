"""
iTaK SEO Analyzer Tool

Analyze content for SEO optimization and competitor research.
Part of Layer 2 (Recon) - SEO-first development principle.

Based on seo_analyzer.py from iTaK's this.md specification.
"""

import os
import json
import re
from typing import List, Optional
from dataclasses import dataclass, field
from urllib.parse import urlparse


@dataclass
class SEOResult:
    """Result from SEO analysis."""
    url: str
    title: str = ""
    meta_description: str = ""
    h1_tags: List[str] = field(default_factory=list)
    h2_tags: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    word_count: int = 0
    issues: List[str] = field(default_factory=list)
    score: int = 0


@dataclass
class CompetitorAnalysis:
    """Analysis of competitor SEO."""
    query: str
    competitors: List[SEOResult] = field(default_factory=list)
    common_keywords: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


def analyze_page(url: str, html_content: str = None) -> SEOResult:
    """Analyze a page for SEO metrics.
    
    Args:
        url: URL of the page
        html_content: Optional HTML content (will fetch if not provided)
        
    Returns:
        SEOResult with analysis
    """
    result = SEOResult(url=url)
    
    if html_content is None:
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(url, timeout=10)
            html_content = response.text
        except ImportError:
            result.issues.append("requests/beautifulsoup4 not installed")
            return result
        except Exception as e:
            result.issues.append(f"Failed to fetch page: {e}")
            return result
    
    try:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Title
        title_tag = soup.find("title")
        if title_tag:
            result.title = title_tag.get_text().strip()
            if len(result.title) < 30:
                result.issues.append("Title too short (<30 chars)")
            elif len(result.title) > 60:
                result.issues.append("Title too long (>60 chars)")
        else:
            result.issues.append("Missing <title> tag")
        
        # Meta description
        meta_desc = soup.find("meta", {"name": "description"})
        if meta_desc and meta_desc.get("content"):
            result.meta_description = meta_desc["content"]
            if len(result.meta_description) < 120:
                result.issues.append("Meta description too short")
            elif len(result.meta_description) > 160:
                result.issues.append("Meta description too long")
        else:
            result.issues.append("Missing meta description")
        
        # H1 tags
        h1s = soup.find_all("h1")
        result.h1_tags = [h.get_text().strip() for h in h1s]
        if len(result.h1_tags) == 0:
            result.issues.append("Missing H1 tag")
        elif len(result.h1_tags) > 1:
            result.issues.append("Multiple H1 tags (should be 1)")
        
        # H2 tags
        h2s = soup.find_all("h2")
        result.h2_tags = [h.get_text().strip() for h in h2s[:10]]
        
        # Word count (main content)
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        words = text.split()
        result.word_count = len(words)
        if result.word_count < 300:
            result.issues.append("Content too thin (<300 words)")
        
        # Extract keywords (simple frequency analysis)
        text_lower = text.lower()
        word_freq = {}
        for word in re.findall(r'\b[a-z]{4,}\b', text_lower):
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Top keywords by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        result.keywords = [word for word, count in sorted_words[:15]]
        
        # Calculate score
        result.score = 100
        result.score -= len(result.issues) * 10
        result.score = max(0, result.score)
        
    except ImportError:
        result.issues.append("beautifulsoup4 not installed")
    except Exception as e:
        result.issues.append(f"Parse error: {e}")
    
    return result


def research_competitors(
    query: str,
    num_results: int = 5,
    searxng_url: str = None,
) -> CompetitorAnalysis:
    """Research top competitors for a search query.
    
    Implements SEO-First Development principle:
    Research competitors before building content.
    
    Args:
        query: Search query
        num_results: Number of top results to analyze
        searxng_url: SearXNG instance URL
        
    Returns:
        CompetitorAnalysis with insights
    """
    searxng_url = searxng_url or os.getenv("SEARXNG_URL", "http://localhost:29541")
    
    print(f"🔍 SEO-FIRST: Researching competitors for '{query}'...")
    
    analysis = CompetitorAnalysis(query=query)
    
    try:
        import requests
        
        # Search via SearXNG
        params = {
            "q": query,
            "format": "json",
            "engines": "google,bing",
        }
        
        response = requests.get(f"{searxng_url}/search", params=params, timeout=15)
        results = response.json().get("results", [])[:num_results]
        
        # Analyze each result
        for result in results:
            url = result.get("url", "")
            seo_result = analyze_page(url)
            seo_result.title = result.get("title", seo_result.title)
            analysis.competitors.append(seo_result)
        
        # Extract common keywords
        all_keywords = []
        for comp in analysis.competitors:
            all_keywords.extend(comp.keywords)
        
        # Count frequencies
        keyword_freq = {}
        for kw in all_keywords:
            keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
        
        # Keywords appearing in multiple competitors
        analysis.common_keywords = [
            kw for kw, count in keyword_freq.items() 
            if count >= 2
        ][:20]
        
        # Generate recommendations
        if analysis.common_keywords:
            analysis.recommendations.append(
                f"Include these keywords: {', '.join(analysis.common_keywords[:5])}"
            )
        
        avg_word_count = sum(c.word_count for c in analysis.competitors) / len(analysis.competitors) if analysis.competitors else 0
        analysis.recommendations.append(
            f"Target word count: {int(avg_word_count * 1.1)} words (10% more than average)"
        )
        
    except ImportError:
        analysis.recommendations.append("Install requests: pip install requests")
    except Exception as e:
        analysis.recommendations.append(f"Search error: {e}")
    
    return analysis


def generate_seo_brief(topic: str) -> dict:
    """Generate an SEO content brief based on competitor research.
    
    Args:
        topic: The topic to create content about
        
    Returns:
        Dictionary with content brief
    """
    analysis = research_competitors(topic)
    
    brief = {
        "topic": topic,
        "target_keywords": analysis.common_keywords[:10],
        "recommendations": analysis.recommendations,
        "competitor_titles": [c.title for c in analysis.competitors if c.title],
        "competitor_h2s": list(set(h2 for c in analysis.competitors for h2 in c.h2_tags))[:10],
    }
    
    return brief


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python seo_analyzer.py <url_or_query>")
        print("Examples:")
        print("  python seo_analyzer.py https://example.com  # Analyze page")
        print("  python seo_analyzer.py 'python tutorial'   # Research competitors")
        sys.exit(1)
    
    target = sys.argv[1]
    
    if target.startswith("http"):
        result = analyze_page(target)
        print(json.dumps({
            "url": result.url,
            "title": result.title,
            "score": result.score,
            "issues": result.issues,
            "keywords": result.keywords,
        }, indent=2))
    else:
        analysis = research_competitors(target)
        print(json.dumps({
            "query": analysis.query,
            "num_competitors": len(analysis.competitors),
            "common_keywords": analysis.common_keywords,
            "recommendations": analysis.recommendations,
        }, indent=2))
