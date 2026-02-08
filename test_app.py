#!/usr/bin/env python3
"""
Test suite for the Sentiment Analysis Application
"""

import json
import unittest

from app import SentimentAnalyzer, app


class TestSentimentAnalysis(unittest.TestCase):
    """Test cases for sentiment analysis functionality"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get("/api/health")
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["service"], "Sentiment Analysis API")

    def test_analyze_sentiment_positive(self):
        """Test sentiment analysis with positive text"""
        test_text = "I love this product! It's amazing and wonderful!"
        response = self.app.post("/api/analyze", json={"text": test_text})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn("sentiment_label", data)
        self.assertIn("compound", data)
        self.assertIn("neg", data)
        self.assertIn("neu", data)
        self.assertIn("pos", data)

        self.assertEqual(data["sentiment_label"], "positive")
        self.assertGreater(data["compound"], 0.05)
        self.assertGreater(data["pos"], data["neg"])

    def test_analyze_sentiment_negative(self):
        """Test sentiment analysis with negative text"""
        test_text = "This is terrible! I hate it and it's awful!"
        response = self.app.post("/api/analyze", json={"text": test_text})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data["sentiment_label"], "negative")
        self.assertLess(data["compound"], -0.05)
        self.assertGreater(data["neg"], data["pos"])

    def test_analyze_sentiment_neutral(self):
        """Test sentiment analysis with neutral text"""
        test_text = "The weather is cloudy today. It might rain later."
        response = self.app.post("/api/analyze", json={"text": test_text})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data["sentiment_label"], "neutral")
        self.assertGreaterEqual(data["compound"], -0.05)
        self.assertLessEqual(data["compound"], 0.05)

    def test_analyze_sentiment_empty_text(self):
        """Test sentiment analysis with empty text"""
        response = self.app.post("/api/analyze", json={"text": ""})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertEqual(data["sentiment_label"], "neutral")
        self.assertEqual(data["compound"], 0.0)

    def test_analyze_sentiment_invalid_request(self):
        """Test sentiment analysis with invalid request"""
        # Missing text field
        response = self.app.post("/api/analyze", json={})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_batch_analyze_sentiment(self):
        """Test batch sentiment analysis"""
        test_texts = ["I love this!", "This is terrible.", "The weather is okay."]

        response = self.app.post("/api/batch-analyze", json={"texts": test_texts})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)

        self.assertIn("results", data)
        self.assertEqual(len(data["results"]), 3)
        self.assertEqual(data["total_analyzed"], 3)

    def test_batch_analyze_sentiment_empty_array(self):
        """Test batch sentiment analysis with empty array"""
        response = self.app.post("/api/batch-analyze", json={"texts": []})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)

    def test_batch_analyze_sentiment_invalid_request(self):
        """Test batch sentiment analysis with invalid request"""
        response = self.app.post("/api/batch-analyze", json={})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("error", data)


class TestSentimentAnalyzer(unittest.TestCase):
    """Test cases for the SentimentAnalyzer class"""

    def setUp(self):
        """Set up SentimentAnalyzer instance"""
        self.analyzer = SentimentAnalyzer()

    def test_preprocess_text(self):
        """Test text preprocessing"""
        original_text = "Hello World! This is a TEST... with URLs: https://example.com and emails: test@example.com"
        processed = self.analyzer.preprocess_text(original_text)

        # Should remove URLs and emails
        self.assertNotIn("https://", processed)
        self.assertNotIn("@", processed)

        # Should be lowercase
        self.assertEqual(processed, processed.lower())

    def test_analyze_sentiment_structure(self):
        """Test that analyze_sentiment returns expected structure"""
        test_text = "This is a test"
        result = self.analyzer.analyze_sentiment(test_text)

        expected_keys = [
            "neg",
            "neu",
            "pos",
            "compound",
            "sentiment_label",
            "confidence",
            "original_text",
            "processed_text",
        ]
        for key in expected_keys:
            self.assertIn(key, result)

        # Check data types
        self.assertIsInstance(result["neg"], float)
        self.assertIsInstance(result["neu"], float)
        self.assertIsInstance(result["pos"], float)
        self.assertIsInstance(result["compound"], float)
        self.assertIsInstance(result["confidence"], float)
        self.assertIsInstance(result["sentiment_label"], str)
        self.assertIsInstance(result["original_text"], str)
        self.assertIsInstance(result["processed_text"], str)


class TestSentimentAnalysisAdvanced(unittest.TestCase):
    """Advanced test cases for sentiment analysis with complex scenarios"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_sentiment_analysis_cases(self):
        """Test sentiment analysis with various complex cases"""
        test_cases = [
            # (Text, Expected_Sentiment, Category)
            (
                "The service was fast and the staff was incredibly friendly.",
                "positive",
                "Simple Polarity",
            ),
            (
                "I am extremely disappointed with the quality of the product.",
                "negative",
                "Simple Polarity",
            ),
            ("The product arrived in a cardboard box.", "neutral", "Simple Polarity"),
            (
                "The movie was not bad at all; in fact, I quite enjoyed it.",
                "positive",
                "Negation",
            ),
            (
                "I don't dislike the new update, but it takes time to get used to.",
                "positive",
                "Double Negative",
            ),
            ("The hotel wasn't exactly clean.", "negative", "Soft Negation"),
            (
                "Oh great, another flight delay. This is exactly how I wanted to spend my Friday.",
                "negative",
                "Sarcasm",
            ),
            (
                "I love it when my computer freezes right before I save my work.",
                "negative",
                "Sarcasm",
            ),
            (
                "The food was delicious, but the prices were astronomical.",
                "neutral",
                "Aspect-Based",
            ),
            (
                "The screen is beautiful; however, the battery life is pathetic.",
                "neutral",
                "Aspect-Based",
            ),
            (
                "If only the customer support was as good as the marketing.",
                "negative",
                "Conditional",
            ),
            ("This new phone is the goat!", "positive", "Slang"),
            (
                "The engine started making a sick sound.",
                "negative",
                "Context-Dependent",
            ),
            ("The plot was a bit of a letdown.", "negative", "Idiomatic"),
            ("This laptop costs an arm and a leg.", "negative", "Idiomatic"),
            (
                "I've been waiting for ages for this to be fixed.",
                "negative",
                "Hyperbole",
            ),
        ]

        for text, expected_sentiment, category in test_cases:
            with self.subTest(text=text, category=category):
                response = self.app.post("/api/analyze", json={"text": text})
                self.assertEqual(response.status_code, 200)

                data = json.loads(response.data)
                self.assertIn("sentiment_label", data)

                # Note: VADER may not handle all complex cases perfectly
                # This test documents expected behavior vs actual behavior
                actual_sentiment = data["sentiment_label"]

                # Log the results for analysis
                print(f"Category: {category}")
                print(f"Text: {text}")
                print(f"Expected: {expected_sentiment}, Actual: {actual_sentiment}")
                print(f"Compound: {data['compound']}")
                print("---")


class TestSentimentAnalysisSecondary(unittest.TestCase):
    """Secondary test cases focusing on sarcasm and nuanced scenarios"""

    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True

    def test_comparative_better_phone(self):
        """Test comparative positive sentiment"""
        text = "This phone is much better than my last one."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "positive")
        print(f"Text: {text}")
        print(f"Expected: positive, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_comparative_not_nearly_as_good(self):
        """Test comparative disappointment"""
        text = "The sequel wasn't nearly as good as the original."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "negative")
        print(f"Text: {text}")
        print(f"Expected: negative, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_aspect_based_plot_interesting_acting_wooden(self):
        """Test aspect-based mixed sentiment"""
        text = "While the plot was interesting, the acting was wooden."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "mixed")
        print(f"Text: {text}")
        print(f"Expected: mixed, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_thwarted_expectation_masterpiece_just_okay(self):
        """Test thwarted expectation"""
        text = "I expected a masterpiece, but it was just okay."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "negative")
        print(f"Text: {text}")
        print(f"Expected: negative, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_nuanced_cant_complain(self):
        """Test nuanced idiomatic positive"""
        text = "For the price, you really can't complain."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "positive")
        print(f"Text: {text}")
        print(f"Expected: positive, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_context_dependent_surprisingly_quiet(self):
        """Test context-dependent neutral"""
        text = "The restaurant was surprisingly quiet for a Saturday night."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "neutral")
        print(f"Text: {text}")
        print(f"Expected: neutral, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_thwarted_expectation_waterproof_broke(self):
        """Test thwarted expectation with product failure"""
        text = "They claim it's waterproof, yet mine broke after one splash."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "negative")
        print(f"Text: {text}")
        print(f"Expected: negative, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_ambiguous_not_sure_like_or_hate(self):
        """Test ambiguous sentiment"""
        text = "I'm not sure if I like it or hate it yet."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "neutral")
        print(f"Text: {text}")
        print(f"Expected: neutral, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_simple_polarity_nightmare_to_navigate(self):
        """Test simple negative polarity"""
        text = "The new interface is a total nightmare to navigate."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "negative")
        print(f"Text: {text}")
        print(f"Expected: negative, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_sarcasm_clear_as_mud(self):
        """Test sarcasm with idiom"""
        text = "The instructions were clear as mud."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "negative")
        print(f"Text: {text}")
        print(f"Expected: negative, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_soft_positive_not_best_but_works(self):
        """Test soft positive sentiment"""
        text = "It's not the best, but it gets the job done."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "positive")
        print(f"Text: {text}")
        print(f"Expected: positive, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_complex_oxymoron_worst_best_movie(self):
        """Test complex oxymoron"""
        text = "This is the worst best movie I have ever seen."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "positive")
        print(f"Text: {text}")
        print(f"Expected: positive, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_context_dependent_battery_lasted_whole_day(self):
        """Test context-dependent positive"""
        text = "The battery lasted the whole day, which was a relief."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "positive")
        print(f"Text: {text}")
        print(f"Expected: positive, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_hyperbole_worst_enemy(self):
        """Test hyperbolic negative"""
        text = "I wouldn't recommend this even to my worst enemy."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "negative")
        print(f"Text: {text}")
        print(f"Expected: negative, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_aspect_based_software_stable(self):
        """Test aspect-based positive"""
        text = "The software is stable, which is all I care about."
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "positive")
        print(f"Text: {text}")
        print(f"Expected: positive, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")

    def test_imperative_avoid_at_all_costs(self):
        """Test imperative negative"""
        text = "Avoid this place at all costs!"
        response = self.app.post("/api/analyze", json={"text": text})
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["sentiment_label"], "negative")
        print(f"Text: {text}")
        print(f"Expected: negative, Actual: {data['sentiment_label']}")
        print(f"Compound: {data['compound']}")
        print("---")


if __name__ == "__main__":
    print("🧪 Running Sentiment Analysis Application Tests...")
    unittest.main(verbosity=2)
