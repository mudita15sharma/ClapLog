"""
API Client for connecting Streamlit to Django REST API.
"""
import os
import requests
import streamlit as st
from typing import Optional, Dict, List


class APIClient:
    """Client for ClapLog Django API."""

    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.token = None

    def _get_headers(self) -> Dict[str, str]:
        """Get headers with auth token."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def login(self, username: str, password: str) -> Optional[str]:
        """Login and get JWT token."""
        url = f"{self.base_url}/auth/login/"
        data = {"username": username, "password": password}

        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                tokens = response.json()
                self.token = tokens['access']
                return self.token
            else:
                st.error(f"Login failed: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def register(self, data: Dict) -> Optional[Dict]:
        """Register new user."""
        url = f"{self.base_url}/users/"

        try:
            response = requests.post(url, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Registration failed: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def verify_email(self, token: str) -> Optional[Dict]:
        """Verify email with token."""
        url = f"{self.base_url}/users/verify_email/"

        try:
            response = requests.post(url, json={"token": token})
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Verification failed: {response.json().get('error', 'Unknown error')}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def resend_verification(self, email: str) -> bool:
        """Resend verification email."""
        url = f"{self.base_url}/users/resend_verification/"

        try:
            response = requests.post(url, json={"email": email})
            if response.status_code == 200:
                return True
            return False
        except:
            return False

    def get_current_user(self) -> Optional[Dict]:
        """Get current user info."""
        url = f"{self.base_url}/users/me/"

        try:
            response = requests.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def _handle_response(self, response) -> List[Dict]:
        """Handle paginated or non-paginated API responses."""
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                if 'results' in data:
                    return data['results']
                return [data]
            elif isinstance(data, list):
                return data
        return []


    def create_production(self, data: Dict) -> Optional[Dict]:
        """Create new production."""
        url = f"{self.base_url}/productions/"

        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def get_productions(self) -> List[Dict]:
        """
        GET /api/productions/
        Returns list of productions WITH scene_count, shot_count,
        completed_scene_count automatically included by the serializer.
        """
        try:
            response = requests.get(
                f"{self.base_url}/productions/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('results', data) if isinstance(data, dict) else data
            else:
                st.error(f"❌ Failed to load productions: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"❌ Connection error: {e}")
            return []

    def get_production(self, production_id: int) -> Dict:
        """
        GET /api/productions/{id}/
        Returns single production with all stats.
        """
        try:
            response = requests.get(
                f"{self.base_url}/productions/{production_id}/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"❌ Error fetching production: {e}")
            return {}

    def get_production_stats(self, production_id: int) -> Optional[Dict]:
        """
        GET /api/productions/{id}/statistics/
        Returns detailed stats: scene breakdown, shot count, completion %.
        """
        try:
            response = requests.get(
                f"{self.base_url}/productions/{production_id}/statistics/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            st.error(f"❌ Error fetching statistics: {e}")
            return {}

    def get_scenes(self, production_id: Optional[int] = None) -> List[Dict]:
        """Get scenes."""
        url = f"{self.base_url}/scenes/"
        if production_id:
            url += f"?production_id={production_id}"

        try:
            response = requests.get(url, headers=self._get_headers())
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching scenes: {str(e)}")
            return []

    def create_scene(self, data: Dict) -> Optional[Dict]:
        """Create new scene."""
        url = f"{self.base_url}/scenes/"

        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def update_scene_status(self, scene_id: int, status: str) -> bool:
        """Update scene status."""
        url = f"{self.base_url}/scenes/{scene_id}/update_status/"

        try:
            response = requests.patch(
                url,
                json={"status": status},
                headers=self._get_headers()
            )
            return response.status_code == 200
        except:
            return False

    def get_shots(self, scene_id: Optional[int] = None) -> List[Dict]:
        """Get shots."""
        url = f"{self.base_url}/shots/"
        if scene_id:
            url += f"?scene_id={scene_id}"

        try:
            response = requests.get(url, headers=self._get_headers())
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching shots: {str(e)}")
            return []

    def create_shot(self, data: Dict) -> Optional[Dict]:
        """Create new shot."""
        url = f"{self.base_url}/shots/"

        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def get_call_sheets(self, production_id: Optional[int] = None) -> List[Dict]:
        """Get call sheets."""
        url = f"{self.base_url}/call-sheets/"
        if production_id:
            url += f"?production={production_id}"

        try:
            response = requests.get(url, headers=self._get_headers())
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching call sheets: {str(e)}")
            return []

    def create_call_sheet(self, data: Dict) -> Optional[Dict]:
        """Create new call sheet."""
        url = f"{self.base_url}/call-sheets/"

        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def get_continuity_notes(self, production_id) -> List[Dict]:
        """Get continuity notes."""
        url = f"{self.base_url}/continuity/"

        try:
            response = requests.get(url, headers=self._get_headers())
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching continuity notes: {str(e)}")
            return []

    def create_continuity_note(self, data: Dict) -> Optional[Dict]:
        """Create continuity note."""
        url = f"{self.base_url}/continuity/"

        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def update_production(self, production_id: int, data: Dict) -> Optional[Dict]:
        """
        PATCH /api/productions/{id}/
        Update any production fields.
        """
        try:
            response = requests.patch(
                f"{self.base_url}/productions/{production_id}/",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json=data
            )
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"❌ Update failed: {response.status_code}")
                return {}
        except Exception as e:
            st.error(f"❌ Error updating production: {e}")
            return {}

    def update_production_status(self, production_id: int, new_status: str) -> bool:
        """
        PATCH /api/productions/{id}/update_status/
        Quick status update.
        """
        try:
            response = requests.patch(
                f"{self.base_url}/productions/{production_id}/update_status/",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json={"status": new_status}
            )
            return response.status_code == 200
        except Exception as e:
            st.error(f"❌ Error updating status: {e}")
            return False

    def delete_production(self, production_id: int) -> bool:
        """
        DELETE /api/productions/{id}/
        """
        try:
            response = requests.delete(
                f"{self.base_url}/productions/{production_id}/",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            return response.status_code == 204
        except Exception as e:
            st.error(f"❌ Error deleting production: {e}")
            return False

    def update_scene(self, scene_id: int, data: Dict) -> Optional[Dict]:
        """Update scene."""
        url = f"{self.base_url}/scenes/{scene_id}/"
        try:
            response = requests.put(url, json=data, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def delete_scene(self, scene_id: int) -> bool:
        """Delete scene."""
        url = f"{self.base_url}/scenes/{scene_id}/"
        try:
            response = requests.delete(url, headers=self._get_headers())
            return response.status_code == 204
        except:
            return False

    def update_shot(self, shot_id: int, data: Dict) -> Optional[Dict]:
        """Update shot."""
        url = f"{self.base_url}/shots/{shot_id}/"
        try:
            response = requests.put(url, json=data, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def delete_shot(self, shot_id: int) -> bool:
        """Delete shot."""
        url = f"{self.base_url}/shots/{shot_id}/"
        try:
            response = requests.delete(url, headers=self._get_headers())
            return response.status_code == 204
        except:
            return False

    def delete_continuity_note(self, note_id: int) -> bool:
        """Delete continuity note."""
        url = f"{self.base_url}/continuity/{note_id}/"
        try:
            response = requests.delete(url, headers=self._get_headers())
            return response.status_code == 204
        except:
            return False

    def get_cast_members(self, production_id: Optional[int] = None) -> List[Dict]:
        """Get cast members."""
        url = f"{self.base_url}/cast-members/?production={production_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=self._get_headers())
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Error fetching cast members: {str(e)}")
            return []

    def create_cast_member(self, data: Dict) -> Optional[Dict]:
        """Create cast member."""
        url = f"{self.base_url}/cast-members/"

        try:
            response = requests.post(url, json=data, headers=self._get_headers())
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def update_cast_member(self, cast_id: int, data: Dict) -> Optional[Dict]:
        """Update cast member."""
        url = f"{self.base_url}/cast-members/{cast_id}/"

        try:
            response = requests.put(url, json=data, headers=self._get_headers())
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.text}")
                return None
        except Exception as e:
            st.error(f"Connection error: {str(e)}")
            return None

    def delete_cast_member(self, cast_id: int) -> bool:
        """Delete cast member."""
        url = f"{self.base_url}/cast-members/{cast_id}/"

        try:
            response = requests.delete(url, headers=self._get_headers())
            return response.status_code == 204
        except:
            return False

    def get_props(self, production_id: int) -> Optional[List[Dict]]:
        """Get all props for a production."""
        url = f"{self.base_url}/props/?production={production_id}"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', data) if isinstance(data, dict) else data
            else:
                st.error(f"Failed to fetch props: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error fetching props: {str(e)}")
            return []


    def create_prop(self, data: Dict) -> Optional[Dict]:
        """Create a new prop."""
        url = f"{self.base_url}/props/"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Failed to create prop: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error creating prop: {str(e)}")
            return None


    def update_prop(self, prop_id: int, data: Dict) -> Optional[Dict]:
        """Update a prop."""
        url = f"{self.base_url}/props/{prop_id}/"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.patch(url, json=data, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to update prop: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error updating prop: {str(e)}")
            return None


    def update_prop_status(self, prop_id: int, status: str) -> bool:
        """Quick update prop status."""
        url = f"{self.base_url}/props/{prop_id}/update_status/"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.patch(url, json={"status": status}, headers=headers)
            return response.status_code == 200
        except:
            return False


    def delete_prop(self, prop_id: int) -> bool:
        """Delete a prop."""
        url = f"{self.base_url}/props/{prop_id}/"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.delete(url, headers=headers)
            return response.status_code == 204
        except:
            return False


    def get_continuity_notes(self, production_id: int = None) -> List[Dict]:
        """Get continuity notes, optionally filtered by production."""
        if production_id:
            url = f"{self.base_url}/continuity-notes/?production={production_id}"
        else:
            url = f"{self.base_url}/continuity-notes/"

        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get('results', data) if isinstance(data, dict) else data
            else:
                st.error(f"Failed to fetch continuity notes: {response.status_code}")
                return []
        except Exception as e:
            st.error(f"Error fetching continuity notes: {str(e)}")
            return []


    def create_continuity_note(self, data: Dict) -> Optional[Dict]:
        """Create a new continuity note."""
        url = f"{self.base_url}/continuity-notes/"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 201:
                return response.json()
            else:
                st.error(f"Failed to create note: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error creating note: {str(e)}")
            return None


    def update_continuity_note(self, note_id: int, data: Dict) -> Optional[Dict]:
        """Update a continuity note."""
        url = f"{self.base_url}/continuity-notes/{note_id}/"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.patch(url, json=data, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Failed to update note: {response.status_code}")
                return None
        except Exception as e:
            st.error(f"Error updating note: {str(e)}")
            return None


    def delete_continuity_note(self, note_id: int) -> bool:
        """Delete a continuity note."""
        url = f"{self.base_url}/continuity-notes/{note_id}/"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.delete(url, headers=headers)
            return response.status_code == 204
        except:
            return False

    def update_scene_status(self, scene_id: int, new_status: str) -> bool:
        """
        PATCH /api/scenes/{id}/
        Update scene status so dashboard completion rate updates.
        Valid statuses: not_started, in_progress, completed, on_hold
        """
        try:
            response = requests.patch(
                f"{self.base_url}/scenes/{scene_id}/",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                },
                json={"status": new_status}
            )
            return response.status_code == 200
        except Exception as e:
            st.error(f"❌ Error updating scene status: {e}")
            return False
