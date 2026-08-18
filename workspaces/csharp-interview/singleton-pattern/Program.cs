// ============================================================
// C# Interview Question - Top 5 Coding Questions #5
// "Write a singleton design pattern and how to implement it in C#"
// Source: SimplyLearn - C# Interview Questions and Answers
// ============================================================

using System;
using System.Threading.Tasks;

namespace CSharpInterview
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("=== Singleton Pattern Demo ===\n");

            // Test 1: Basic singleton usage
            Console.WriteLine("--- Test 1: Basic Usage ---");
            Singleton s1 = Singleton.Instance;
            Singleton s2 = Singleton.Instance;

            Console.WriteLine($"s1.Id = {s1.Id}");
            Console.WriteLine($"s2.Id = {s2.Id}");
            Console.WriteLine($"Same instance? {ReferenceEquals(s1, s2)}");

            // Test 2: Thread safety demo
            Console.WriteLine("\n--- Test 2: Thread Safety ---");
            Parallel.Invoke(
                () => Console.WriteLine($"Thread 1: {Singleton.Instance.Id}"),
                () => Console.WriteLine($"Thread 2: {Singleton.Instance.Id}"),
                () => Console.WriteLine($"Thread 3: {Singleton.Instance.Id}")
            );

            // Test 3: Lazy initialization demo
            Console.WriteLine("\n--- Test 3: Lazy<T> Version ---");
            LazySingleton ls1 = LazySingleton.Instance;
            LazySingleton ls2 = LazySingleton.Instance;
            Console.WriteLine($"Same instance? {ReferenceEquals(ls1, ls2)}");

            Console.WriteLine("\nPress any key to exit...");
            Console.ReadKey();
        }
    }

    // ============================================================
    // APPROACH 1: Classic Thread-Safe Singleton (Double-Check Locking)
    // ============================================================
    public sealed class Singleton
    {
        private static Singleton _instance;
        private static readonly object _lock = new object();
        public int Id { get; }

        private Singleton()
        {
            Id = new Random().Next(1000, 9999);
            Console.WriteLine($"[Singleton] Created instance with Id = {Id}");
        }

        public static Singleton Instance
        {
            get
            {
                // First check (no lock) - fast path
                if (_instance == null)
                {
                    lock (_lock)
                    {
                        // Second check (with lock) - ensures only one created
                        if (_instance == null)
                        {
                            _instance = new Singleton();
                        }
                    }
                }
                return _instance;
            }
        }
    }

    // ============================================================
    // APPROACH 2: Lazy<T> Singleton (Modern, Clean, Thread-Safe)
    // ============================================================
    public sealed class LazySingleton
    {
        private static readonly Lazy<LazySingleton> _instance =
            new Lazy<LazySingleton>(() => new LazySingleton());

        public int Id { get; }

        private LazySingleton()
        {
            Id = new Random().Next(1000, 9999);
            Console.WriteLine($"[LazySingleton] Created instance with Id = {Id}");
        }

        public static LazySingleton Instance => _instance.Value;
    }

    // ============================================================
    // APPROACH 3: Eager Initialization (Simple, Thread-Safe)
    // ============================================================
    public sealed class EagerSingleton
    {
        private static readonly EagerSingleton _instance = new EagerSingleton();

        public int Id { get; }

        private EagerSingleton()
        {
            Id = new Random().Next(1000, 9999);
            Console.WriteLine($"[EagerSingleton] Created instance with Id = {Id}");
        }

        public static EagerSingleton Instance => _instance;
    }
}