import networkx as nx

class BehavioralGraph:
    """
    Models the user's behavioral ecosystem as a graph.
    Nodes: Habits, Metrics (e.g., Deep Work)
    Edges: Correlations / Associations
    """
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph(self, user_id, habits, correlations):
        """
        Builds the behavioral graph for a given user.
        """
        self.graph.clear()
        
        # Add nodes
        for habit in habits:
            self.graph.add_node(habit['id'], type='habit', label=habit['name'])
            
        # Add edges (correlations)
        for corr in correlations:
            if corr['source_id'] in self.graph and corr['target_id'] in self.graph:
                self.graph.add_edge(
                    corr['source_id'], 
                    corr['target_id'], 
                    weight=corr['correlation_strength']
                )
                
    def get_graph_data(self):
        """
        Serializes graph for frontend visualization.
        """
        data = nx.node_link_data(self.graph)
        return data

    def detect_central_habits(self):
        """
        Finds habits with the most influence (highest degree centrality).
        """
        centrality = nx.degree_centrality(self.graph)
        sorted_habits = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
        return sorted_habits
