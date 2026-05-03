interface PasswordStrengthProps {
  password: string;
}

export default function PasswordStrength({ password }: PasswordStrengthProps) {
  const getStrength = (pwd: string): { score: number; label: string; color: string } => {
    if (!pwd) return { score: 0, label: '', color: '' };
    
    let score = 0;
    
    // Length
    if (pwd.length >= 8) score++;
    if (pwd.length >= 12) score++;
    
    // Complexity
    if (/[a-z]/.test(pwd)) score++;
    if (/[A-Z]/.test(pwd)) score++;
    if (/[0-9]/.test(pwd)) score++;
    if (/[^a-zA-Z0-9]/.test(pwd)) score++;
    
    // Normalize to 0-4
    const normalizedScore = Math.min(Math.floor(score / 1.5), 4);
    
    const labels = ['', 'Weak', 'Fair', 'Strong', 'Very Strong'];
    const colors = ['', 'bg-danger', 'bg-warning', 'bg-success', 'bg-green-600'];
    
    return {
      score: normalizedScore,
      label: labels[normalizedScore],
      color: colors[normalizedScore],
    };
  };

  const strength = getStrength(password);
  
  if (!password) return null;

  return (
    <div className="mt-2">
      <div className="flex gap-1 mb-1">
        {[1, 2, 3, 4].map((level) => (
          <div
            key={level}
            className={`h-1 flex-1 rounded-full transition-colors ${
              level <= strength.score ? strength.color : 'bg-gray-200'
            }`}
          />
        ))}
      </div>
      {strength.label && (
        <p className="text-xs text-gray-600">
          Password strength: <span className="font-medium">{strength.label}</span>
        </p>
      )}
    </div>
  );
}
