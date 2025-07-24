export interface NetworkFlow {
  FlowID: number;
  FlowDuration: number;
  Src: string;
  SrcPort: number;
  Dest: string;
  DestPort: number;
  Protocol: string;
  Classification: string;
  Probability: number;
  Risk: string;
  FlowStartTime: string;
  FlowLastSeen: string;
  PName?: string;
  PID?: string;
  [key: string]: any;
}

export interface IPData {
  SourceIP: string;
  count: number;
}

export interface SocketResponse {
  result: any[];
  ips: IPData[];
}

export interface FlowDetail extends NetworkFlow {
  explanation?: string;
  ae_plot?: string;
}