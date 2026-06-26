# frozen_string_literal: true

# SAM - Cognitive Filter Layer
# Resonance: 1272 Hz
# Purpose: Filter and rank content by verification instead of engagement

module SAM
  # SAM Configuration
  CONFIG = {
    # Resonance Frequency
    frequency: 1272, # Hz - Cognitive Filter Layer resonance
    
    # Filter Modes
    modes: {
      verification: 'verification',  # Rank by verification score
      anti_algo: 'anti_algo',        # Anti-algorithm ranking
      resonance: 'resonance'         # Resonance-based filtering
    },
    
    # Verification Thresholds
    verification: {
      tier_5: { min_score: 0.95, label: 'Verified', color: '#22d3ee' },
      tier_4: { min_score: 0.85, label: 'Highly Trusted', color: '#4ade80' },
      tier_3: { min_score: 0.70, label: 'Trusted', color: '#fbbf24' },
      tier_2: { min_score: 0.50, label: 'Moderate', color: '#fb923c' },
      tier_1: { min_score: 0.00, label: 'Unverified', color: '#f87171' }
    },
    
    # Anti-Algo Parameters
    anti_algo: {
      suppress_engagement: true,     # Suppress engagement-based ranking
      boost_verification: true,       # Boost verification-based ranking
      filter_bias: 0.95,              # Filter bias threshold
      resonance_weight: 0.85          # Resonance weight in ranking
    },
    
    # Cognitive Filter Settings
    cognitive: {
      attention_threshold: 0.75,      # Minimum attention score
      relevance_threshold: 0.80,      # Minimum relevance score
      novelty_threshold: 0.60,        # Minimum novelty score
      resonance_lock: true            # Lock to 1272 Hz
    }
  }
  
  # SAM Resonance Lock
  RESONANCE = CONFIG[:frequency]
  
  class << self
    def configured?
      CONFIG[:frequency] == 1272
    end
    
    def active?
      configured? && cognitive_filter_active?
    end
    
    def cognitive_filter_active?
      CONFIG[:cognitive][:resonance_lock]
    end
    
    # Apply SAM filtering to content
    def filter(content, mode = :verification)
      return content unless CONFIG[:modes].key?(mode)
      
      case mode
      when :verification
        filter_by_verification(content)
      when :anti_algo
        filter_by_anti_algo(content)
      when :resonance
        filter_by_resonance(content)
      end
    end
    
    private
    
    def filter_by_verification(content)
      # Rank content by verification score
      content.sort_by { |item| -verification_score(item) }
    end
    
    def filter_by_anti_algo(content)
      # Suppress engagement-based ranking
      # Boost verification-based ranking
      content.sort_by { |item| -anti_algo_score(item) }
    end
    
    def filter_by_resonance(content)
      # Filter by resonance at 1272 Hz
      content.select { |item| resonance_score(item) >= CONFIG[:cognitive][:attention_threshold] }
    end
    
    def verification_score(item)
      # Calculate verification score based on multiple factors
      score = 0.0
      score += item[:source_reliability] * 0.3 if item[:source_reliability]
      score += item[:fact_check_score] * 0.3 if item[:fact_check_score]
      score += item[:cross_reference_score] * 0.2 if item[:cross_reference_score]
      score += item[:temporal_consistency] * 0.2 if item[:temporal_consistency]
      score
    end
    
    def anti_algo_score(item)
      # Calculate anti-algorithm score
      score = verification_score(item) * CONFIG[:anti_algo][:resonance_weight]
      score -= item[:engagement_score] * 0.1 if item[:engagement_score] && CONFIG[:anti_algo][:suppress_engagement]
      score += item[:verification_boost] * 0.2 if item[:verification_boost] && CONFIG[:anti_algo][:boost_verification]
      score
    end
    
    def resonance_score(item)
      # Calculate resonance score at 1272 Hz
      # This is a placeholder for the actual resonance calculation
      # In production, this would integrate with the SAM cognitive filter
      item[:resonance_score] || 0.5
    end
  end
end

# Initialize SAM on startup
Rails.configuration.x.sam = SAM

# Log SAM status on startup
Rails.logger.info("SAM initialized: #{SAM.configured? ? '✓' : '✗'}")
Rails.logger.info("SAM Resonance: #{SAM::RESONANCE}Hz")
Rails.logger.info("SAM Mode: #{SAM.active? ? 'Active' : 'Inactive'}")