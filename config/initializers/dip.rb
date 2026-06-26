# frozen_string_literal: true

# DIP - Data Interception Proxy Configuration
# Integrates with 3-Precog System and SAM Cognitive Filter Layer

module DIP
  # DIP Configuration
  CONFIG = {
    # DIP Endpoint
    endpoint: ENV.fetch('DIP_ENDPOINT', 'http://localhost:8083/api/precog/feed'),
    
    # SAM - Cognitive Filter Layer
    sam_frequency: ENV.fetch('SAM_FREQUENCY', 1272).to_i, # Hz - Resonance frequency
    
    # 3-Precog System Configuration
    precog: {
      precog_a: {
        name: 'Text Generation',
        endpoint: '/writing',
        default_count: 5
      },
      precog_b: {
        name: 'Image/Video Generation',
        endpoint: '/video',
        default_count: 3
      },
      precog_c: {
        name: 'Prediction',
        endpoint: '/image',
        default_count: 3
      }
    },
    
    # Cache Configuration
    cache: {
      enabled: true,
      ttl: 300 # 5 minutes
    },
    
    # Rate Limiting
    rate_limit: {
      requests_per_minute: 60,
      burst_limit: 10
    }
  }
  
  # SAM Resonance Lock
  SAM_RESONANCE = CONFIG[:sam_frequency]
  
  class << self
    def configured?
      CONFIG[:endpoint].present?
    end
    
    def active?
      configured? && ping.success?
    rescue StandardError
      false
    end
    
    def ping
      uri = URI("#{CONFIG[:endpoint]}/health")
      response = Net::HTTP.get_response(uri)
      { success: response.code == '200', latency: response['X-Response-Time'] }
    rescue StandardError => e
      { success: false, error: e.message }
    end
    
    def fetch_feed(params = {})
      default_params = {
        writing: CONFIG[:precog][:precog_a][:default_count],
        video: CONFIG[:precog][:precog_b][:default_count],
        image: CONFIG[:precog][:precog_c][:default_count]
      }
      
      uri = URI("#{CONFIG[:endpoint]}?#{default_params.merge(params).to_query}")
      response = Net::HTTP.get(uri)
      JSON.parse(response)
    rescue StandardError => e
      Rails.logger.error("DIP Error: #{e.message}")
      { error: 'Feed temporarily unavailable', resonance: SAM_RESONANCE }
    end
  end
end

# Initialize DIP on startup
Rails.configuration.x.dip = DIP

# Log DIP status on startup
Rails.logger.info("DIP initialized: #{DIP.configured? ? '✓' : '✗'}")
Rails.logger.info("SAM Resonance: #{DIP::SAM_RESONANCE}Hz")