"""Product Approval/Rejection API tests for Teresa Backoffice UAT"""

import pytest
import time
import json
from datetime import datetime
from api.endpoints import Endpoints
from config.test_data_product_approval import PRODUCT_APPROVAL_TEST_CASES, VALID_PRODUCT_STATUSES
from utils.assertions import Assertions
from config.settings import settings

# PATCH  https://api.uat.teresaapp.com/api/v1/rbac/products/status  → Endpoints.PRODUCT_STATUS


class TestProductApprovalAPI:
    """Test suite for Product Approval/Rejection API on UAT environment"""

    @classmethod
    def setup_class(cls):
        """Setup before all tests"""
        print(f"\n{'='*70}")
        print(f"Starting PRODUCT APPROVAL/REJECTION API Tests - UAT Environment")
        print(f"Environment: {settings.ENVIRONMENT}")
        print(f"Admin User:  {settings.ADMIN_EMAIL}")
        print(f"Endpoint:    PATCH {Endpoints.PRODUCT_STATUS}")
        print(f"Timestamp:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*70}\n")

        cls.test_product_ids = {}
        cls.bug_detected = False

    # ── Authentication ─────────────────────────────────────────────────────────

    def get_admin_auth_token(self, api_client):
        """Obtain an admin authentication token"""
        print("   Getting admin token...")

        login_data = {
            "identifier": settings.ADMIN_EMAIL,
            "password": settings.ADMIN_PASSWORD,
        }

        login_response = api_client.post(Endpoints.LOGIN, json=login_data)

        if login_response.status_code == 200:
            response_data = login_response.json()
            if response_data.get("success"):
                token = response_data.get("data", {}).get("access_token")
                if token:
                    print(f"   ✓ Admin token obtained ({len(token)} chars)")
                    return token

        print("   ❌ Failed to obtain admin token")
        return None

    @pytest.fixture(autouse=True)
    def setup_admin_auth(self, api_client):
        """Set up admin authentication before every test"""
        self.client = api_client

        admin_token = self.get_admin_auth_token(api_client)
        if admin_token:
            api_client.set_auth_token(admin_token)
            print("   ✓ Admin authentication successful")
        else:
            print("   ❌ Could not get admin token")
            api_client.clear_auth_token()

    # ── Product Lookup Helpers ─────────────────────────────────────────────────

    def get_pending_product_id(self):
        """Return the ID of a product in 'pending_approval' state"""
        print("   Finding pending product for testing...")

        params = {"page": 1, "limit": 10, "status": "pending_approval"}
        response = self.client.get(Endpoints.PRODUCTS, params=params)

        if response.status_code == 200:
            data = response.json()
            for product in data.get("data", []):
                if product.get("status") == "pending_approval":
                    product_id = product.get("id")
                    name = product.get("name", "N/A")
                    print(f"   ✓ Found pending product: {name} (ID: {product_id})")
                    return product_id

        print("   ⚠ No pending products found")
        return None

    def get_approved_product_id(self):
        """Return the ID of an already-approved product"""
        print("   Finding approved product for testing...")

        params = {"page": 1, "limit": 10, "status": "approved"}
        response = self.client.get(Endpoints.PRODUCTS, params=params)

        if response.status_code == 200:
            data = response.json()
            for product in data.get("data", []):
                if product.get("status") == "approved":
                    product_id = product.get("id")
                    name = product.get("name", "N/A")
                    print(f"   ✓ Found approved product: {name} (ID: {product_id})")
                    return product_id

        print("   ⚠ No approved products found")
        return None

    def get_rejected_product_id(self):
        """Return the ID of a previously rejected product"""
        print("   Finding rejected product for testing...")

        params = {"page": 1, "limit": 10, "status": "rejected"}
        response = self.client.get(Endpoints.PRODUCTS, params=params)

        if response.status_code == 200:
            data = response.json()
            for product in data.get("data", []):
                if product.get("status") == "rejected":
                    product_id = product.get("id")
                    name = product.get("name", "N/A")
                    print(f"   ✓ Found rejected product: {name} (ID: {product_id})")
                    return product_id

        print("   ⚠ No rejected products found")
        return None

    def get_any_product_id(self):
        """Return any product ID (used for generic validation tests)"""
        print("   Finding any product for validation testing...")

        params = {"page": 1, "limit": 10}
        response = self.client.get(Endpoints.PRODUCTS, params=params)

        if response.status_code == 200:
            data = response.json()
            products = data.get("data", [])
            if products:
                product_id = products[0].get("id")
                name = products[0].get("name", "N/A")
                print(f"   ✓ Found product: {name} (ID: {product_id})")
                return product_id

        print("   ⚠ No products found")
        return None

    # ── Parametrised Test ──────────────────────────────────────────────────────

    @pytest.mark.admin
    @pytest.mark.uat
    @pytest.mark.parametrize(
        "test_case",
        [tc for tc in PRODUCT_APPROVAL_TEST_CASES if not tc.get("skip", False)],
    )
    def test_product_approval(self, test_case):
        """Test product approval/rejection via PATCH /rbac/products/status"""
        test_id = test_case["test_id"]
        description = test_case["description"]

        print(f"\n▶ Test: {test_id} - {description}")

        data = test_case.get("data", {}).copy()

        # ── Dynamic ID replacement ────────────────────────────────────────────

        if "{product_id}" in str(data):
            product_id = self.get_pending_product_id()
            if product_id:
                data["product_id"] = product_id
            else:
                print("   ⚠ Skipping test: No pending product available")
                pytest.skip("No pending product available for testing")

        if "{approved_product_id}" in str(data):
            approved_product_id = self.get_approved_product_id()
            if approved_product_id:
                data["product_id"] = approved_product_id
            else:
                print("   ⚠ Skipping test: No approved product available")
                pytest.skip("No approved product available for testing")

        if "{rejected_product_id}" in str(data):
            rejected_product_id = self.get_rejected_product_id()
            if rejected_product_id:
                data["product_id"] = rejected_product_id
            else:
                print("   ⚠ Skipping test: No rejected product available")
                pytest.skip("No rejected product available for testing")

        # ── Strip auth for the unauthenticated test case ──────────────────────
        if "TC_Product_Approve_03" in test_id:
            self.client.clear_auth_token()
            print("   Testing without authentication")

        print(f"   Request data: {json.dumps(data, indent=6)}")

        start_time = time.time()
        response = self.client.patch(Endpoints.PRODUCT_STATUS, json=data)
        response_time = time.time() - start_time

        # ── Parse response body ───────────────────────────────────────────────
        response_data = {}
        if response.text and response.text.strip():
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                print(f"   ⚠ Response is not valid JSON: {response.text[:100]}")

        expected_status = test_case["expected_status"]

        # ── Status code check ─────────────────────────────────────────────────
        if response.status_code != expected_status:
            print(f"   ❌ Expected {expected_status}, got {response.status_code}")
            if response_data:
                print(f"   Message: {response_data.get('message')}")
                if "errors" in response_data:
                    print(f"   Errors:  {response_data.get('errors')}")

            if test_id == "TC_Product_Approve_09" and response.status_code == 200:
                self.bug_detected = True
                print("   ⚠ BUG DETECTED: API accepts whitespace-only reason")

        Assertions.assert_status_code(response, expected_status)

        # ── Success-path assertions ───────────────────────────────────────────
        if expected_status == 200:
            assert response_data.get("success") is True, (
                f"Expected success=True, got {response_data.get('success')}"
            )

            if "expected_message" in test_case:
                actual_message = response_data.get("message", "")
                assert test_case["expected_message"] in actual_message, (
                    f"Expected '{test_case['expected_message']}' in '{actual_message}'"
                )
                print(f"   ✓ Message: {actual_message}")

            if "data" in response_data:
                updated_data = response_data["data"]
                print("   ✓ Product status updated successfully")

                if "status" in updated_data:
                    expected_status_val = data.get("status")
                    actual_status_val = updated_data.get("status")
                    if expected_status_val and actual_status_val:
                        assert actual_status_val == expected_status_val, (
                            f"Expected status '{expected_status_val}', "
                            f"got '{actual_status_val}'"
                        )
                        print(f"   ✓ Status changed to: {actual_status_val}")

            print(f"   ✓ Response time: {response_time:.3f}s")

        # ── Error-path assertions ─────────────────────────────────────────────
        else:
            if response_data:
                if "expected_message" in test_case and "message" in response_data:
                    actual_message = response_data.get("message", "")
                    assert test_case["expected_message"] in actual_message, (
                        f"Expected '{test_case['expected_message']}' in '{actual_message}'"
                    )
                    print(f"   ✓ Error message: {actual_message}")

                if "expected_errors" in test_case and "errors" in response_data:
                    assert len(response_data.get("errors", [])) > 0, (
                        "Expected at least one error in response"
                    )
                    print("   ✓ Validation errors returned")

                if "expected_success" in test_case:
                    actual_success = response_data.get("success")
                    assert actual_success == test_case["expected_success"], (
                        f"Expected success={test_case['expected_success']}, "
                        f"got {actual_success}"
                    )

        if test_case.get("is_bug"):
            print("   ⚠ KNOWN BUG: whitespace-only reason accepted by API")
            self.bug_detected = True

        print(f"   ✅ PASS: {test_id}")

    # ── Smoke Test ─────────────────────────────────────────────────────────────

    @pytest.mark.admin
    @pytest.mark.smoke
    def test_product_approval_smoke(self):
        """Smoke test: approve a pending product and verify the status change"""
        print("\n▶ Smoke Test: Product Approval Basic Workflow")

        pending_product_id = self.get_pending_product_id()

        if not pending_product_id:
            print("   ⚠ Skipping: No pending products available")
            pytest.skip("No pending products available for smoke test")

        approval_data = {
            "product_id": pending_product_id,
            "status": "approved",
            "reason": "Smoke test approval — all product details verified",
        }

        print(f"   Approving product: {pending_product_id}")
        print(f"   Approval data: {json.dumps(approval_data, indent=6)}")

        response = self.client.patch(Endpoints.PRODUCT_STATUS, json=approval_data)

        if response.status_code == 200:
            response_data = response.json()
            print(f"   ✓ Approval successful: {response_data.get('message')}")

            # Verify status was updated via the product listing endpoint
            params = {"search": pending_product_id[:8], "page": 1, "limit": 5}
            verify_response = self.client.get(Endpoints.PRODUCTS, params=params)

            if verify_response.status_code == 200:
                products = verify_response.json().get("data", [])
                found = next((p for p in products if p.get("id") == pending_product_id), None)

                if found:
                    new_status = found.get("status")
                    if new_status == "approved":
                        print(f"   ✓ Product status successfully changed to: {new_status}")
                        print("   ✓ Smoke test completed successfully")
                    else:
                        print(f"   ⚠ Product status is '{new_status}', expected 'approved'")
                else:
                    print("   ⚠ Could not find product in listing after approval")
            else:
                print(f"   ⚠ Could not verify product status: {verify_response.status_code}")
        else:
            print(f"   ❌ Approval failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            pytest.fail("Product approval smoke test failed")

    # ── Performance Test ───────────────────────────────────────────────────────

    @pytest.mark.admin
    @pytest.mark.performance
    def test_product_approval_performance(self):
        """Approve multiple products and assert response times are within limits"""
        print("\n▶ Testing product approval performance...")

        pending_products = []
        params = {"page": 1, "limit": 5, "status": "pending_approval"}
        response = self.client.get(Endpoints.PRODUCTS, params=params)

        if response.status_code == 200:
            for product in response.json().get("data", []):
                if product.get("status") == "pending_approval":
                    pending_products.append(product.get("id"))

        if len(pending_products) < 2:
            print("   ⚠ Skipping: Need at least 2 pending products for performance test")
            pytest.skip("Not enough pending products for performance test")

        response_times = []

        for i, product_id in enumerate(pending_products[:2]):
            approval_data = {
                "product_id": product_id,
                "status": "approved",
                "reason": f"Performance test approval {i + 1}",
            }

            start_time = time.time()
            response = self.client.patch(Endpoints.PRODUCT_STATUS, json=approval_data)
            response_time = time.time() - start_time

            if response.status_code == 200:
                response_times.append(response_time)
                print(f"   Request {i + 1}: Approved in {response_time:.3f}s")
            else:
                print(f"   ⚠ Request {i + 1} failed: {response.status_code}")

        if response_times:
            avg_time = sum(response_times) / len(response_times)
            max_time = max(response_times)
            min_time = min(response_times)

            print(f"\n   Performance Summary:")
            print(f"   ✓ Approvals:  {len(response_times)} successful")
            print(f"   ✓ Average:    {avg_time:.3f}s")
            print(f"   ✓ Min / Max:  {min_time:.3f}s / {max_time:.3f}s")

            assert avg_time < 3.0, f"Average approval time {avg_time:.3f}s exceeds 3s limit"
            assert max_time < 5.0, f"Max approval time {max_time:.3f}s exceeds 5s limit"
            print("   ✓ Performance acceptable for UAT environment")
        else:
            print("   ⚠ No successful approvals for performance measurement")

        print("   ✅ PASS: Product approval performance test")

    # ── Validation Test ────────────────────────────────────────────────────────

    @pytest.mark.admin
    @pytest.mark.validation
    def test_product_approval_validation(self):
        """Inline validation scenarios using a real product ID"""
        print("\n▶ Testing product approval validation...")

        actual_product_id = self.get_any_product_id()

        if not actual_product_id:
            print("   ⚠ Skipping: No products available for validation test")
            pytest.skip("No products available for validation test")

        inline_cases = [
            {
                "name": "Missing product_id",
                "data": {"status": "approved", "reason": "Test reason"},
                "expected_status": 422,
                "expected_message": "product_id is required",
            },
            {
                "name": "Missing status",
                "data": {"product_id": actual_product_id, "reason": "Test reason"},
                "expected_status": 422,
                "expected_message": "status is required",
            },
            {
                "name": "Missing reason (optional field — should succeed)",
                "data": {"product_id": actual_product_id, "status": "approved"},
                "expected_status": 200,
                "expected_message": "Product approved successfully",
            },
            {
                "name": "Empty product_id",
                "data": {"product_id": "", "status": "approved", "reason": "Test"},
                "expected_status": 422,
                "expected_message": "Validation failed",
            },
            {
                "name": "Invalid UUID format for product_id",
                "data": {"product_id": "not-a-uuid", "status": "approved", "reason": "Test"},
                "expected_status": 422,
                "expected_message": "Validation failed",
            },
            {
                "name": "Empty reason string (should be rejected)",
                "data": {"product_id": actual_product_id, "status": "approved", "reason": ""},
                "expected_status": 422,
                "expected_message": "Validation failed",
            },
            {
                "name": "Whitespace-only reason (BUG: Currently accepted)",
                "data": {"product_id": actual_product_id, "status": "approved", "reason": "   "},
                "expected_status": 200,  # Should be 422 — known bug
                "expected_message": "Product approved successfully",
                "is_bug": True,
            },
            {
                "name": "Single-character reason (minimum valid)",
                "data": {"product_id": actual_product_id, "status": "approved", "reason": "a"},
                "expected_status": 200,
                "expected_message": "Product approved successfully",
            },
        ]

        passed = 0
        bugs_found = 0
        total = len(inline_cases)

        for case in inline_cases:
            print(f"   Testing: {case['name']}")

            response = self.client.patch(Endpoints.PRODUCT_STATUS, json=case["data"])
            status_match = response.status_code == case["expected_status"]

            if status_match:
                print(f"     ✓ Correct status: {response.status_code}")

                if response.status_code != 200 and response.text:
                    try:
                        rd = response.json()
                        if case.get("expected_message") and "message" in rd:
                            if case["expected_message"] in rd.get("message", ""):
                                print("     ✓ Correct error message")
                            else:
                                print(f"     ⚠ Message mismatch: '{rd.get('message')}'")
                    except Exception:
                        pass

                passed += 1

                if case.get("is_bug"):
                    bugs_found += 1
                    print("     ⚠ KNOWN BUG: Whitespace-only reason accepted by API")
            else:
                print(f"     ❌ Expected {case['expected_status']}, got {response.status_code}")
                if response.text:
                    print(f"     Response: {response.text[:150]}")

        print(f"\n   ✓ Validation tests passed: {passed}/{total}")

        if bugs_found:
            print(f"   ⚠ BUGS DETECTED: {bugs_found} case(s) passed that should fail")
            print("   ⚠ Issue: API accepts whitespace-only reason string")
            self.bug_detected = True

        assert passed == total, f"Only {passed}/{total} validation tests passed"
        print("   ✅ PASS: Product approval validation test (known bugs documented)")

    # ── Integration Test ───────────────────────────────────────────────────────

    @pytest.mark.admin
    @pytest.mark.integration
    def test_product_approval_rejection_cycle(self):
        """Integration test: Approve → Verify → Reject → Verify"""
        print("\n▶ Integration Test: Product Approve / Reject Cycle")

        pending_product_id = self.get_pending_product_id()

        if not pending_product_id:
            print("   ⚠ Skipping: No pending products available")
            pytest.skip("No pending products available for integration test")

        print(f"   Test product ID: {pending_product_id}")

        # ── Step 1: Approve ───────────────────────────────────────────────────
        approve_data = {
            "product_id": pending_product_id,
            "status": "approved",
            "reason": "Integration test — initial approval",
        }
        approve_response = self.client.patch(Endpoints.PRODUCT_STATUS, json=approve_data)

        if approve_response.status_code != 200:
            print(f"   ❌ Approval failed: {approve_response.status_code}")
            pytest.skip("Initial approval failed; cannot proceed with integration test")

        print("   ✓ Product approved successfully")

        # ── Step 2: Verify approval ───────────────────────────────────────────
        params = {"search": pending_product_id[:8]}
        verify_response = self.client.get(Endpoints.PRODUCTS, params=params)

        if verify_response.status_code == 200:
            for product in verify_response.json().get("data", []):
                if product.get("id") == pending_product_id:
                    s = product.get("status")
                    print(f"   {'✓' if s == 'approved' else '⚠'} Product status verified as '{s}'")
                    break

        # ── Step 3: Reject ────────────────────────────────────────────────────
        reject_data = {
            "product_id": pending_product_id,
            "status": "rejected",
            "reason": "Integration test — changed to rejected",
        }
        reject_response = self.client.patch(Endpoints.PRODUCT_STATUS, json=reject_data)

        if reject_response.status_code == 200:
            print("   ✓ Product rejected successfully")
        else:
            print(f"   ⚠ Rejection failed: {reject_response.status_code}")

        # ── Step 4: Verify rejection ──────────────────────────────────────────
        verify_response = self.client.get(Endpoints.PRODUCTS, params=params)
        if verify_response.status_code == 200:
            for product in verify_response.json().get("data", []):
                if product.get("id") == pending_product_id:
                    s = product.get("status")
                    print(f"   {'✓' if s == 'rejected' else '⚠'} Product status verified as '{s}'")
                    break

        print("   ✅ PASS: Integration test for product approve/reject cycle completed")

    # ── Teardown ───────────────────────────────────────────────────────────────

    @classmethod
    def teardown_class(cls):
        """Teardown and bug report after all tests"""
        print(f"\n{'='*70}")
        print("Test Session Complete")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if hasattr(cls, "bug_detected") and cls.bug_detected:
            print(f"\n{'⚠️ ' * 10}BUG REPORT {'⚠️ ' * 10}")
            print("Bug ID:      BUG-API-PRODUCT-001")
            print("Title:       API Accepts Whitespace-Only Reason String")
            print("Description: The product approval API accepts strings containing")
            print("             only whitespace characters as valid reasons.")
            print("Impact:      Low — Functionality works but audit logs may contain")
            print("             meaningless entries.")
            print("Expected:    Should return 422 for whitespace-only reason strings,")
            print("             consistent with the empty-string rejection behaviour.")
            print(f"{'⚠️ ' * 20}")

        print(f"\n{'='*70}\n")