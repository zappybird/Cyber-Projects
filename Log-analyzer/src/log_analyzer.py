#!/usr/bin/env python3
"""
Basic Log Analyzer 
Parses log files, extracts severity levels, and identifies common issues.
"""

import os
import re
from collections import Counter, defaultdict

def find_log_files(directory):
    log_files = []
    for root, _, files in os.walk(directory):
        for f in files:
            if f.endswith(".log") or f.endswith(".txt"):
                log_files.append(os.path.join(root, f))
    return log_files

def load_log_entries(files):
    entries = []
    for path in files:
        try:
            with open(path, "r", errors="replace") as f:
                for line in f:
                    entries.append(line.strip())
        except Exception:
            pass
    return entries

def parse_log_entry(line):
    log_entry = {'raw': line}
    
    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})', line)
    if timestamp_match:
        log_entry["timestamp"] = timestamp_match.group(1)
    
    severity_match = re.search(r'\b(ERROR|INFO|WARNING|DEBUG|CRITICAL|WARN|FATAL)\b', line, re.IGNORECASE)
    if severity_match:
        log_entry["severity"] = severity_match.group(1).upper()
    else:
        log_entry["severity"] = "UNKNOWN"
    
    if timestamp_match:
        remainder = line[timestamp_match.end():].strip()
    else:
        remainder = line
        
    if severity_match:
        component_msg = remainder.replace(severity_match.group(0), "", 1).strip()
        
        component_match = re.search(r'^\[([^\]]+)\]|^([^:]+):', component_msg)
        if component_match:
            component = component_match.group(1) or component_match.group(2)
            log_entry["component"] = component.strip()
            
            if component_match.group(1):
                log_entry["message"] = component_msg[component_match.end():].strip()
            else:
                log_entry["message"] = component_msg[component_match.end():].strip()
        else:
            log_entry["message"] = component_msg
    else:
        log_entry["message"] = remainder
    
    return log_entry

def analyze_log_entries(entries):
    total_entries = len(entries)
    severities = Counter()
    components = Counter()
    errors_by_component = defaultdict(list)
    timestamps = []
    
    for entry in entries:
        parsed = parse_log_entry(entry)
        severities[parsed.get('severity', 'UNKNOWN')] += 1
        
        if 'component' in parsed:
            components[parsed['component']] += 1
            if parsed.get('severity') in ['ERROR', 'CRITICAL', 'FATAL']:
                errors_by_component[parsed['component']].append(parsed.get('message', ''))
        
        if 'timestamp' in parsed:
            timestamps.append(parsed['timestamp'])
    
    time_pattern = None
    if timestamps:
        try:
            timestamps = sorted(timestamps)
            time_pattern = {
                'first_occurrence': timestamps[0],
                'last_occurrence': timestamps[-1],
                'total_occurrences': len(timestamps)
            }
        except Exception:
            pass
    
    error_patterns = []
    for component, errors in errors_by_component.items():
        for error in errors:
            if error and len(error) > 10:
                pattern = re.sub(r'\b[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}\b', '<ID>', error)
                pattern = re.sub(r'\d+', '<NUM>', pattern)
                error_patterns.append((component, pattern))
    
    common_patterns = Counter(error_patterns).most_common(10)
    
    formatted_patterns = [
        {'component': comp, 'pattern': pat, 'count': count}
        for (comp, pat), count in common_patterns
    ]
    
    return {
        'total_entries': total_entries,
        'severity_distribution': dict(severities),
        'components': dict(components),
        'time_pattern': time_pattern,
        'error_patterns': formatted_patterns,
        'entries': [parse_log_entry(e) for e in entries]
    }

def suggest_solutions(analysis):
    solutions = []

    for item in analysis.get('error_patterns', []):
        if not isinstance(item.get('pattern'), str):
            item['pattern'] = str(item.get('pattern', ''))

    connection_errors = any(
        'connection' in item['pattern'].lower() or
        'timeout' in item['pattern'].lower() or
        'connect' in item['pattern'].lower()
        for item in analysis.get('error_patterns', [])
    )
    
    if connection_errors:
        solutions.append({
            'problem': 'Connection issues',
            'solution': 'Check network connectivity between services and verify that all dependent services are running. Look for firewall or DNS issues.'
        })
    
    permission_errors = any(
        'permission' in item['pattern'].lower() or
        'access' in item['pattern'].lower() or
        'denied' in item['pattern'].lower()
        for item in analysis.get('error_patterns', [])
    )
    
    if permission_errors:
        solutions.append({
            'problem': 'Permission issues',
            'solution': 'Verify file and resource permissions. Check that service accounts have the necessary access rights.'
        })
    
    resource_errors = any(
        'memory' in item['pattern'].lower() or
        'cpu' in item['pattern'].lower() or
        'capacity' in item['pattern'].lower() or
        'full' in item['pattern'].lower()
        for item in analysis.get('error_patterns', [])
    )
    
    if resource_errors:
        solutions.append({
            'problem': 'Resource constraints',
            'solution': 'Check system resources (memory, CPU, disk space). Consider scaling up infrastructure or optimizing resource usage.'
        })
    
    db_errors = any(
        'database' in item['pattern'].lower() or
        'db' in item['pattern'].lower() or
        'sql' in item['pattern'].lower() or
        'query' in item['pattern'].lower()
        for item in analysis.get('error_patterns', [])
    )
    
    if db_errors:
        solutions.append({
            'problem': 'Database issues',
            'solution': 'Check database connectivity, query performance, and database logs. Verify that database indices are properly set up.'
        })
    
    if not solutions:
        if analysis.get('total_entries', 0) > 0:
            components = analysis.get('components', {})
            most_common_component = max(components.items(), key=lambda x: x[1])[0] if components else 'unknown'
            
            solutions.append({
                'problem': f'Multiple errors in {most_common_component} component',
                'solution': f'Review the {most_common_component} component logs in detail and check recent code changes or configuration updates to this component.'
            })
    
    return solutions

def main():
    directory = "./logs"
    files = find_log_files(directory)
    entries = load_log_entries(files)
    analysis = analyze_log_entries(entries)
    suggestions = suggest_solutions(analysis)

    print("\n--- Log Analysis Summary ---")
    print("Total Entries:", analysis["total_entries"])
    print("Severity Distribution:", analysis["severity_distribution"])
    print("Top Components:", analysis["components"])

    print("\nError Patterns:")
    for item in analysis["error_patterns"]:
        print(f"  {item['count']}x [{item['component']}] {item['pattern']}")

    print("\nSuggestions:")
    for s in suggestions:
        print(f" - {s['problem']}: {s['solution']}")

if __name__ == "__main__":
    main()
