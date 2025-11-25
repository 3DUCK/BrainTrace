import sys
import json
import random

def main():
    """
    Demo Agent for Pricing/ROI Prediction.
    
    Expected Input (JSON):
    {
        "question": "What if we reduce ad spend by 20%?",
        "params": { "reduction_rate": 20 } (Optional)
    }
    
    Output (JSON):
    {
        "answer": "Predicted ROI increase is 5%...",
        "data": { ... }
    }
    """
    try:
        # Read input from command line argument
        if len(sys.argv) < 2:
            print(json.dumps({"error": "No input provided"}))
            return

        input_str = sys.argv[1]
        input_data = json.loads(input_str)
        
        question = input_data.get("question", "")
        params = input_data.get("params", {})
        
        # Mock Logic based on question keywords
        if "광고비" in question or "ad spend" in question.lower():
            reduction = params.get("reduction_rate", 20) # Default to 20 if not parsed
            roi_change = random.uniform(3.0, 8.0)
            answer = (
                f"광고비를 {reduction}% 줄일 경우, 단기적으로 노출 수는 감소하지만 "
                f"타겟팅 최적화를 통해 ROI는 약 {roi_change:.1f}% 개선될 것으로 예측됩니다. "
                f"다만, 신규 고객 유입은 약 10-15% 감소할 위험이 있습니다."
            )
            result = {
                "answer": answer,
                "data": {
                    "roi_change": roi_change,
                    "traffic_loss": 12.5
                }
            }
            
        elif "가격" in question or "price" in question.lower():
            answer = (
                "현재 시장 경쟁 상황과 원가 구조를 분석한 결과, "
                "기존 가격 대비 5% 인상이 이익률 극대화에 도움이 될 것으로 보입니다. "
                "프리미엄 기능을 추가하여 가격 저항을 낮추는 전략을 권장합니다."
            )
            result = {
                "answer": answer,
                "data": {
                    "recommended_increase": 5,
                    "margin_improvement": 2.3
                }
            }
            
        else:
            # Default fallback for other agent questions
            answer = (
                f"요청하신 '{question}'에 대한 분석 결과입니다. "
                "현재 데이터로는 명확한 예측이 어려우나, 긍정적인 추세가 예상됩니다."
            )
            result = {
                "answer": answer,
                "data": {}
            }

        # Print JSON output to stdout
        print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        error_response = {
            "error": str(e),
            "status": "failed"
        }
        print(json.dumps(error_response))

if __name__ == "__main__":
    main()
