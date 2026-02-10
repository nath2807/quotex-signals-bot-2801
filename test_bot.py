"""Simple tests for the Quotex Signals Bot."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from signal_generator import SignalGenerator
from config import Config


def test_signal_generator():
    """Test signal generator initialization and basic functionality."""
    print("Testing Signal Generator...")
    
    # Test initialization
    generator = SignalGenerator(confidence_threshold=70)
    assert generator.confidence_threshold == 70
    print("✓ Signal generator initialized correctly")
    
    # Test signal generation
    signal = generator.generate_signal("EURUSD")
    if signal:
        assert 'pair' in signal
        assert 'type' in signal
        assert 'timeframe' in signal
        assert 'confidence' in signal
        assert signal['type'] in ['CALL', 'PUT']
        assert signal['timeframe'] in ['1m', '5m', '15m', '30m', '1h']
        print("✓ Signal generated successfully")
        print(f"  Signal details: {signal['pair']} - {signal['type']} - {signal['confidence']}%")
    else:
        print("✓ No signal generated (below threshold)")
    
    # Test multiple pairs analysis
    pairs = ['EURUSD', 'GBPUSD', 'USDJPY']
    signals = generator.analyze_multiple_pairs(pairs)
    print(f"✓ Analyzed {len(pairs)} pairs, generated {len(signals)} signals")
    
    # Test message formatting
    if signals:
        message = generator.format_signal_message(signals[0])
        assert len(message) > 0
        assert signals[0]['pair'] in message
        print("✓ Signal message formatted correctly")


def test_config():
    """Test configuration loading."""
    print("\nTesting Configuration...")
    
    # Test validation
    is_valid = Config.validate()
    assert is_valid
    print("✓ Configuration validated")
    
    # Test default values
    assert Config.SIGNAL_INTERVAL > 0
    assert Config.CONFIDENCE_THRESHOLD >= 0 and Config.CONFIDENCE_THRESHOLD <= 100
    assert len(Config.TRADING_PAIRS) > 0
    print(f"✓ Configuration loaded: {len(Config.TRADING_PAIRS)} trading pairs")


def test_signal_format():
    """Test signal message format."""
    print("\nTesting Signal Format...")
    
    generator = SignalGenerator()
    test_signal = {
        'pair': 'EURUSD',
        'type': 'CALL',
        'timeframe': '5m',
        'confidence': 85,
        'timestamp': '2024-01-01T12:00:00',
        'entry_price': 1.08500
    }
    
    message = generator.format_signal_message(test_signal)
    assert 'EURUSD' in message
    assert 'CALL' in message
    assert '5m' in message
    assert '85' in message
    print("✓ Signal format test passed")
    print(f"\nSample signal output:\n{message}")


def run_all_tests():
    """Run all tests."""
    print("="*50)
    print("Running Quotex Signals Bot Tests")
    print("="*50 + "\n")
    
    try:
        test_config()
        test_signal_generator()
        test_signal_format()
        
        print("\n" + "="*50)
        print("✅ All tests passed!")
        print("="*50)
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
