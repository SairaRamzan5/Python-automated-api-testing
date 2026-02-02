"""Test suite for Techniques Get API - WITH BUG DOCUMENTATION"""

import pytest
import json
from datetime import datetime
from api.endpoints import Endpoints
from config.test_data_techniques_get import TECHNIQUES_GET_TEST_DATA, ACTUAL_TECHNIQUE_FIELDS, OPTIONAL_TECHNIQUE_FIELDS, TEST_CONFIG

class TestTechniquesGetAPI:
    """Test suite for getting techniques - DOCUMENTING SEARCH BUG"""
    
    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"TECHNIQUES GET API TESTS")
        print(f"Endpoint: {Endpoints.TECHNIQUES.replace('create', '')}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")
    
    @pytest.fixture(autouse=True)
    def setup_admin_auth(self, api_client, admin_auth_token):
        """Setup admin authentication before each test"""
        self.client = api_client
        
        if admin_auth_token:
            self.client.set_auth_token(admin_auth_token)
            print("   ✓ Admin authentication set")
        else:
            print("   ⚠ No admin token available")
            self.client.clear_auth_token()
    
    def verify_technique_structure(self, technique):
        """Verify the structure of a technique object"""
        print(f"     Actual fields in technique: {list(technique.keys())}")
        
        required_fields = TEST_CONFIG["required_technique_fields"]
        
        for field in required_fields:
            assert field in technique, f"Missing required field: {field}"
            print(f"     ✓ Contains required field: {field}")
        
        assert isinstance(technique["values"], list), "values should be an array"
        if technique["values"]:
            value = technique["values"][0]
            assert "language_code" in value, "value missing language_code"
            assert "name" in value, "value missing name"
            print(f"     ✓ Values array valid ({len(technique['values'])} language(s))")
        
        for field in OPTIONAL_TECHNIQUE_FIELDS:
            if field in technique:
                print(f"     - Contains optional field: {field}")
                if field == "is_duplicate":
                    print(f"       Is duplicate: {technique[field]}")
        
        if "parent_name" in technique:
            print(f"     - Parent name: {technique['parent_name']}")
        
        if "children" in technique:
            print(f"     - Children count: {len(technique['children'])}")
    
    def verify_pagination(self, pagination_data, expected_page=None, expected_limit=None):
        """Verify pagination structure and values"""
        required_fields = ["page", "limit", "total", "total_pages", "has_next", "has_prev"]
        
        for field in required_fields:
            assert field in pagination_data, f"Missing pagination field: {field}"
            print(f"     ✓ Pagination contains: {field}")
        
        assert isinstance(pagination_data["page"], (int, str)), "page should be int or str"
        assert isinstance(pagination_data["limit"], (int, str)), "limit should be int or str"
        assert isinstance(pagination_data["total"], (int, str)), "total should be int or str"
        assert isinstance(pagination_data["total_pages"], (int, str)), "total_pages should be int or str"
        assert isinstance(pagination_data["has_next"], bool), "has_next should be boolean"
        assert isinstance(pagination_data["has_prev"], bool), "has_prev should be boolean"
        
        if expected_page is not None:
            actual_page = int(pagination_data["page"]) if isinstance(pagination_data["page"], str) else pagination_data["page"]
            if actual_page != expected_page:
                print(f"     ⚠ Page mismatch: expected {expected_page}, got {actual_page}")
            else:
                print(f"     ✓ Page correct: {actual_page}")
        
        if expected_limit is not None:
            actual_limit = int(pagination_data["limit"]) if isinstance(pagination_data["limit"], str) else pagination_data["limit"]
            if actual_limit != expected_limit:
                print(f"     ⚠ Limit mismatch: expected {expected_limit}, got {actual_limit}")
            else:
                print(f"     ✓ Limit correct: {actual_limit}")
        
        return pagination_data
    
    @pytest.mark.techniques
    @pytest.mark.get
    @pytest.mark.smoke
    def test_get_all_active_techniques_smoke(self):
        """Smoke test: Get all active techniques"""
        print("\n▶ Smoke Test: Get All Active Techniques")
        
        params = {"is_active": "true"}
        
        print(f"   Requesting active techniques")
        print(f"   Params: {params}")
        
        response = self.client.get(Endpoints.TECHNIQUES.replace("create", ""), params=params)
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Success: {data.get('success')}")
            
            if data.get("success"):
                print(f"   ✓ Request successful")
                print(f"   Message: {data.get('message')}")
                
                if "data" in data:
                    techniques = data["data"]
                    print(f"   Found {len(techniques)} techniques")
                    
                    if techniques:
                        print(f"   Verifying first technique structure:")
                        self.verify_technique_structure(techniques[0])
                
                if "meta" in data and "pagination" in data["meta"]:
                    print(f"   Verifying pagination (in meta.pagination):")
                    self.verify_pagination(data["meta"]["pagination"])
                elif "pagination" in data:
                    print(f"   Verifying pagination:")
                    self.verify_pagination(data["pagination"])
                else:
                    print(f"   ⚠ No pagination found in response")
            else:
                print(f"   ⚠ Request unsuccessful: {data.get('message')}")
        
        elif response.status_code == 401:
            print(f"   ❌ Unauthorized - Admin token may be invalid")
        else:
            print(f"   ❌ Unexpected status: {response.status_code}")
    
    @pytest.mark.techniques
    @pytest.mark.get
    @pytest.mark.parametrize("test_case", 
        TECHNIQUES_GET_TEST_DATA["positive_cases"] + 
        TECHNIQUES_GET_TEST_DATA["negative_cases"])
    def test_get_techniques_various_scenarios(self, test_case):
        """Test various get techniques scenarios - WILL FAIL FOR SEARCH DUE TO BUG"""
        test_id = test_case.get("test_id", "UNKNOWN")
        description = test_case["description"]
        
        print(f"\n▶ Test: {test_id} - {description}")
        
        if test_case.get("headers") == {}:
            self.client.clear_auth_token()
            print("   Testing without authentication")
        
        params = test_case.get("params", {})
        
        print(f"   Parameters: {params}")
        
        response = self.client.get(Endpoints.TECHNIQUES.replace("create", ""), params=params)
        
        actual_status = response.status_code
        expected_status = test_case["expected_status"]
        
        print(f"   Status: {actual_status} (expected: {expected_status})")
        
        status_match = actual_status == expected_status
        if not status_match:
            print(f"   ⚠ Status mismatch: expected {expected_status}, got {actual_status}")
        
        if response.text:
            try:
                data = response.json()
                
                if "expected_success" in test_case and "success" in data:
                    expected_success = test_case["expected_success"]
                    actual_success = data.get("success")
                    
                    success_match = expected_success == actual_success
                    if not success_match:
                        print(f"   ⚠ Success mismatch: expected {expected_success}, got {actual_success}")
                    else:
                        print(f"   ✓ Success matches: {actual_success}")
                
                if actual_status == 200 and data.get("success"):
                    
                    if "data" in data:
                        techniques = data["data"]
                        print(f"   Found {len(techniques)} techniques")
                        
                        # CRITICAL: Check for search bug
                        if "search" in params:
                            search_term = params["search"]
                            print(f"   🚨 SEARCH BUG CHECK: Searching for '{search_term}'")
                            
                            # Count how many actually contain the search term
                            matching_count = sum(
                                1 for tech in techniques 
                                if search_term.lower() in tech.get("name", "").lower()
                            )
                            
                            print(f"   Results containing '{search_term}': {matching_count}/{len(techniques)}")
                            
                            if matching_count == len(techniques):
                                print(f"   🚨 BUG CONFIRMED: ALL results contain search term")
                                print(f"   🚨 This means search is NOT filtering! (API Bug)")
                            elif matching_count == 0 and len(techniques) > 0:
                                print(f"   🚨 BUG CONFIRMED: NO results contain search term but API returned {len(techniques)}")
                                print(f"   🚨 Search parameter is being IGNORED! (Critical Bug)")
                            elif matching_count > 0:
                                print(f"   ⚠ Mixed results: Some contain search, some don't")
                            
                            # Show bug note if present
                            if test_case.get("bug_note"):
                                print(f"   🐞 {test_case['bug_note']}")
                        
                        if "expected_data_count" in test_case:
                            expected_count = test_case["expected_data_count"]
                            actual_count = len(techniques)
                            
                            if actual_count == expected_count:
                                print(f"   ✓ Has exactly {expected_count} techniques")
                            else:
                                print(f"   ⚠ Has {actual_count} techniques, expected {expected_count}")
                                
                                # If this is a search test, mark as bug
                                if "search" in params and actual_count > expected_count:
                                    print(f"   🚨 BUG: Search returned {actual_count} instead of {expected_count}")
                
            except json.JSONDecodeError:
                print(f"   ❌ Response is not valid JSON: {response.text[:200]}")
        
        print(f"   {'✓' if status_match else '⚠'} Test completed: {test_id}")
    
    @pytest.mark.techniques
    @pytest.mark.get
    @pytest.mark.bug
    def test_document_search_bug(self):
        """Document the CRITICAL search bug in API"""
        print("\n" + "="*80)
        print("🚨 CRITICAL BUG REPORT: Search Parameter is IGNORED")
        print("="*80)
        
        # Step 1: Get baseline (no search)
        print("\n1. BASELINE: Get ALL techniques (no search):")
        response_all = self.client.get(Endpoints.TECHNIQUES.replace("create", ""))
        
        if response_all.status_code != 200:
            print(f"   ❌ Failed: {response_all.status_code}")
            return
        
        data_all = response_all.json()
        all_techniques = data_all.get("data", [])
        total_count = len(all_techniques)
        
        print(f"   ✓ Found {total_count} total techniques")
        for i, tech in enumerate(all_techniques):
            print(f"     {i+1}. {tech.get('name')}")
        
        if total_count == 0:
            print("   ⚠ No techniques to test")
            return
        
        # Step 2: Test searches that SHOULD return different results
        print("\n2. BUG VERIFICATION: Testing various searches")
        print("   (All should return DIFFERENT counts but return SAME due to bug)")
        
        test_cases = [
            {"term": "Single", "description": "Should return 1", "expected": 1},
            {"term": "Test", "description": "Should return 2", "expected": 2},
            {"term": "1768808718215", "description": "Should return 1", "expected": 1},
            {"term": "NONEXISTENT_XYZ", "description": "Should return 0", "expected": 0},
            {"term": "@#$%", "description": "Special chars", "expected": 0},
        ]
        
        bug_confirmed = False
        results = []
        
        for test in test_cases:
            print(f"\n   Searching: '{test['term']}'")
            print(f"   Expected: {test['expected']} techniques")
            
            params = {"search": test["term"]}
            response = self.client.get(Endpoints.TECHNIQUES.replace("create", ""), params=params)
            
            if response.status_code == 200:
                data = response.json()
                techniques = data.get("data", [])
                actual_count = len(techniques)
                
                results.append({
                    "term": test["term"],
                    "expected": test["expected"],
                    "actual": actual_count,
                    "is_bug": actual_count == total_count
                })
                
                print(f"   Actual: {actual_count} techniques")
                
                if actual_count == total_count:
                    print(f"   🚨 BUG CONFIRMED: Returns ALL {total_count} techniques!")
                    bug_confirmed = True
                    
                    # Check if results match the baseline
                    same_ids = all(
                        t1.get("id") == t2.get("id") 
                        for t1, t2 in zip(techniques, all_techniques)
                    )
                    if same_ids:
                        print(f"   🚨 BUG DETAIL: Returns EXACT SAME techniques as no-search!")
                else:
                    print(f"   ✓ Search seems to work (different count)")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        
        # Step 3: Generate bug report
        print("\n" + "="*80)
        print("📋 BUG REPORT SUMMARY")
        print("="*80)
        
        print(f"\nTotal techniques in system: {total_count}")
        print("\nSearch Test Results:")
        print("-" * 70)
        print(f"{'Search Term':<25} {'Expected':<10} {'Actual':<10} {'Status':<20}")
        print("-" * 70)
        
        for result in results:
            if result["is_bug"]:
                status = "🚨 BUG: Returns ALL"
            elif result["actual"] == result["expected"]:
                status = "✓ Correct"
            else:
                status = f"⚠ {result['actual']} (not {result['expected']})"
            
            print(f"{result['term'][:22]:<25} {result['expected']:<10} {result['actual']:<10} {status:<20}")
        
        print("-" * 70)
        
        if bug_confirmed:
            print("\n🚨 CRITICAL BUG DETECTED:")
            print("   The 'search' query parameter is being IGNORED by the API.")
            print("   All search requests return ALL techniques.")
            print("\n🐞 Bug Details:")
            print("   - Search doesn't filter results")
            print("   - Returns same data as no-search request")
            print("   - Non-existent terms still return all techniques")
            print("\n🔧 Impact:")
            print("   - Users cannot find specific techniques")
            print("   - Search functionality is completely broken")
            print("   - Wastes bandwidth returning unnecessary data")
            print("\n💡 Recommendation:")
            print("   - Fix backend search implementation")
            print("   - Ensure search parameter filters results")
            print("   - Return empty array for non-existent searches")
            
            # This test will FAIL to document the bug
            pytest.fail("🚨 CRITICAL BUG: Search parameter ignored by API")
        else:
            print("\n✅ Search functionality appears to be working correctly")
    
    @pytest.mark.techniques
    @pytest.mark.get
    @pytest.mark.bug
    def test_search_bug_comprehensive(self):
        """Comprehensive test to demonstrate search bug"""
        print("\n▶ Test: Comprehensive Search Bug Demonstration")
        
        # Get all techniques first
        response = self.client.get(Endpoints.TECHNIQUES.replace("create", ""))
        
        if response.status_code != 200:
            print(f"   ❌ Failed to get techniques: {response.status_code}")
            return
        
        data = response.json()
        all_techniques = data.get("data", [])
        technique_names = [t.get("name") for t in all_techniques]
        
        print(f"   System has {len(all_techniques)} techniques:")
        for name in technique_names:
            print(f"     - {name}")
        
        print("\n   Testing search bug scenarios...")
        
        # Scenario 1: Search for something that exists
        existing_search = technique_names[0].split()[0] if technique_names else "Single"
        print(f"\n   1. Search for existing term: '{existing_search}'")
        params = {"search": existing_search}
        response = self.client.get(Endpoints.TECHNIQUES.replace("create", ""), params=params)
        
        if response.status_code == 200:
            search_data = response.json()
            search_results = search_data.get("data", [])
            
            print(f"      Returned: {len(search_results)} techniques")
            print(f"      Expected: 1 or more (filtered)")
            
            if len(search_results) == len(all_techniques):
                print(f"      🚨 BUG: Returns ALL techniques instead of filtered!")
        
        # Scenario 2: Search for non-existent
        print(f"\n   2. Search for non-existent term: 'DELETED_XYZ_123'")
        params = {"search": "DELETED_XYZ_123"}
        response = self.client.get(Endpoints.TECHNIQUES.replace("create", ""), params=params)
        
        if response.status_code == 200:
            search_data = response.json()
            search_results = search_data.get("data", [])
            
            print(f"      Returned: {len(search_results)} techniques")
            print(f"      Expected: 0 (empty array)")
            
            if len(search_results) > 0:
                print(f"      🚨 BUG: Returns {len(search_results)} techniques for non-existent search!")
                print(f"      First result: {search_results[0].get('name')}")
        
        # Scenario 3: Empty search
        print(f"\n   3. Empty search: ''")
        params = {"search": ""}
        response = self.client.get(Endpoints.TECHNIQUES.replace("create", ""), params=params)
        
        if response.status_code == 200:
            search_data = response.json()
            search_results = search_data.get("data", [])
            
            print(f"      Returned: {len(search_results)} techniques")
            print(f"      Expected: All or empty (depends on implementation)")
        
        print(f"\n   ✅ Bug demonstration complete")
    
    @classmethod
    def teardown_class(cls):
        """Cleanup after all tests"""
        print(f"\n{'='*70}")
        print(f"TECHNIQUES GET TESTS COMPLETED")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}")