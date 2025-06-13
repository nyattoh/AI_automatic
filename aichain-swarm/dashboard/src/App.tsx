import { useEffect } from 'react';
import { Box, Flex } from '@chakra-ui/react';
import { atom, useRecoilState } from 'recoil';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const tokenAtom = atom<number[]>({ key: 'tokens', default: [] });
const sessionAtom = atom<{ active: number; idle: number }>({ key: 'sessions', default: { active: 0, idle: 0 } });

export default function App() {
  const [tokens, setTokens] = useRecoilState(tokenAtom);
  const [session, setSession] = useRecoilState(sessionAtom);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/stream');
    ws.onmessage = (ev) => {
      const data = JSON.parse(ev.data);
      setTokens((t) => [...t.slice(-59), data.tokens || 0]);
      setSession((s) => ({ ...s, active: data.active || s.active }));
    };
    return () => ws.close();
  }, [setTokens, setSession]);

  return (
    <Flex height="100vh" p={4} gap={4} align="stretch">
      <Box flex="1">
        <Bar
          data={{
            labels: tokens.map((_, i) => String(i)),
            datasets: [{ label: 'Tokens', data: tokens, backgroundColor: 'teal' }],
          }}
        />
      </Box>
      <Box width="300px">
        <Pie
          data={{
            labels: ['Active', 'Idle'],
            datasets: [{ data: [session.active, session.idle], backgroundColor: ['green', 'gray'] }],
          }}
        />
      </Box>
    </Flex>
  );
}
