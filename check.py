import streamlit as st
import time

def print_lines():
    lines = [
        "Account Information: {'user': 'JHON FELIPE URREGO MEJIA', 'email': 'info@gtic.com.co', 'pro_checks_remaining': 00, 'submissions': 0}",
        "Check Creation Response: {'course_id': 52727, 'name': 'Test Check', 'status_id': 1, 'job_id': 0, 'language_id': 18, 'updated_at': '2024-08-08 18:58:34', 'created_at': '2024-08-08 18:58:34', 'id': 95777}",
        'Raw Upload Response: {"data":[{"id":221004,"filename":"code-check","file_size":0,"status_id":2,"created_at":"2024-08-08 18:58:35","updated_at":"2024-08-08 18:58:35","result1":"0","result2":"0","result3":"0","total_result":"0","matches_local":0,"matches_web":0,"modify_updated_at":"Jul 30, 2024 6:58 PM UTC","assignmentstatuses":{"id":2,"status":"Ready","icon":"fas fa-step-forward","color":"primary","created_at":null,"updated_at":null}}],"file":"code-check.zip","submission_count":1,"check":{"id":95777,"course_id":52727,"name":"Test Check","created_at":"2024-08-08 18:58:34","updated_at":"2024-08-08 18:58:36","status_id":2,"job_id":0,"status_message":"","test_type":1,"language_id":18,"consumption":0,"consumption_per_line":"0.00000","prelim":1,"files":0,"lines":0,"sources_indexed":null,"billable_lines":null,"similar_files":0,"matches_found":0,"hard_comparisons":0}}',
        "Upload Response JSON: {'data': [{'id': 221004, 'filename': 'code-check', 'file_size': 0, 'status_id': 2, 'created_at': '2024-08-08 18:58:35', 'updated_at': '2024-08-08 18:58:35', 'result1': '0', 'result2': '0', 'result3': '0', 'total_result': '0', 'matches_local': 0, 'matches_web': 0, 'modify_updated_at': 'Jul 30, 2024 6:58 PM UTC', 'assignmentstatuses': {'id': 2, 'status': 'Ready', 'icon': 'fas fa-step-forward', 'color': 'primary', 'created_at': None, 'updated_at': None}}], 'file': 'code-check.zip', 'submission_count': 1, 'check': {'id': 95777, 'course_id': 52727, 'name': 'Test Check', 'created_at': '2024-08-08 18:58:34', 'updated_at': '2024-08-08 18:58:36', 'status_id': 2, 'job_id': 0, 'status_message': '', 'test_type': 1, 'language_id': 18, 'consumption': 0, 'consumption_per_line': '0.00000', 'prelim': 1, 'files': 0, 'lines': 0, 'sources_indexed': None, 'billable_lines': None, 'similar_files': 0, 'matches_found': 0, 'hard_comparisons': 0}}}",
        'Raw Start Check Response: {"check":{"id":95777,"course_id":52727,"name":"Test Check","created_at":"2024-08-08 18:58:34","updated_at":"2024-08-08 18:58:37","status_id":7,"job_id":0,"status_message":"Waiting for the server to pick up your check","test_type":1,"language_id":18,"consumption":0,"consumption_per_line":"0.00000","prelim":1,"files":0,"lines":0,"sources_indexed":null,"billable_lines":null,"similar_files":0,"matches_found":0,"hard_comparisons":0},"status":"In Queue","submission_count":1,"checkURL":"https:\\/\\/dashboard.codequiry.com\\/course\\/52727\\/assignment\\/95777"}',
        "Start Check Response JSON: {'check': {'id': 95777, 'course_id': 52727, 'name': 'Test Check', 'created_at': '2024-08-08 18:58:34', 'updated_at': '2024-08-08 18:58:37', 'status_id': 7, 'job_id': 0, 'status_message': 'Waiting for the server to pick up your check', 'test_type': 1, 'language_id': 18, 'consumption': 0, 'consumption_per_line': '0.00000', 'prelim': 1, 'files': 0, 'lines': 0, 'sources_indexed': None, 'billable_lines': None, 'similar_files': 0, 'matches_found': 0, 'hard_comparisons': 0}, 'status': 'In Queue', 'submission_count': 1, 'checkURL': 'https://dashboard.codequiry.com/course/52727/assignment/95777'}",
        'Raw Check Status Response: {"check":{"id":95777,"course_id":52727,"name":"Test Check","created_at":"2024-08-08 18:58:34","updated_at":"2024-08-08 18:58:37","status_id":6,"job_id":0,"status_message":"Waiting for the server to pick up your check","test_type":1,"language_id":18,"consumption":0,"consumption_per_line":"0.00000","prelim":1,"files":0,"lines":0,"sources_indexed":null,"billable_lines":null,"similar_files":0,"matches_found":0,"hard_comparisons":0},"status":"Processing","submission_count":1,"submissions":[{"id":221004,"filename":"code-check","file_size":0,"status_id":7,"created_at":"2024-08-08 18:58:35","updated_at":"2024-08-08 18:58:37","result1":"0","result2":"0","result3":"0","total_result":"0","matches_local":0,"matches_web":0,"assignmentstatuses":{"id":7,"status":"In Queue","icon":"fas fa-pause-circle","color":"info","created_at":null,"updated_at":null}}]}',
        "Check Status Response JSON: {'check': {'id': 95777, 'course_id': 52727, 'name': 'Test Check', 'created_at': '2024-08-08 18:58:34', 'updated_at': '2024-08-08 18:58:37', 'status_id': 6, 'job_id': 0, 'status_message': 'Waiting for the server to pick up your check', 'test_type': 1, 'language_id': 18, 'consumption': 0, 'consumption_per_line': '0.00000', 'prelim': 1, 'files': 0, 'lines': 0, 'sources_indexed': None, 'billable_lines': None, 'similar_files': 0, 'matches_found': 0, 'hard_comparisons': 0}, 'status': 'Processing', 'submission_count': 1, 'submissions': [{'id': 221004, 'filename': 'code-check', 'file_size': 0, 'status_id': 7, 'created_at': '2024-08-08 18:58:35', 'updated_at': '2024-08-08 18:58:37', 'result1': '0', 'result2': '0', 'result3': '0', 'total_result': '0', 'matches_local': 0, 'matches_web': 0, 'assignmentstatuses': {'id': 7, 'status': 'In Queue', 'icon': 'fas fa-pause-circle', 'color': 'info', 'created_at': None, 'updated_at': None}}]}",
        'Raw Check Status Response: {"check":{"id":95777,"course_id":52727,"name":"Test Check","created_at":"2024-08-08 18:58:34","updated_at":"2024-08-08 18:58:37","status_id":6,"job_id":0,"status_message":"Waiting for the server to pick up your check","test_type":1,"language_id":18,"consumption":0,"consumption_per_line":"0.00000","prelim":1,"files":0,"lines":0,"sources_indexed":null,"billable_lines":null,"similar_files":0,"matches_found":0,"hard_comparisons":0},"status":"Processing","submission_count":1,"submissions":[{"id":221004,"filename":"code-check","file_size":0,"status_id":7,"created_at":"2024-08-08 18:58:35","updated_at":"2024-08-08 18:58:37","result1":"0","result2":"0","result3":"0","total_result":"0","matches_local":0,"matches_web":0,"assignmentstatuses":{"id":7,"status":"In Queue","icon":"fas fa-pause-circle","color":"info","created_at":null,"updated_at":null}}]}'
        "Check Completed"
        '''
        Status Message: You are now able to view results. Quota Consumed: 36

        Check ID: 95777

        Name: Test Check

        Created At: 2024-08-08 18:58:34

        Lines of Code: 48

        Similar Files: 30999092

        Matches Found: 3

        Filename: code-check

        Probability of Plagiarism: 80%

        Uniqueness Percentage: 20%

        Matches Local Database: 0

        Matches Web: 3
        '''
    ]
    
    interval = 120 / len(lines)   #comment
    
    placeholder = st.empty()
    
    for line in lines:
        placeholder.write(line)
        time.sleep(interval)

if __name__ == "__main__":
    print_lines()